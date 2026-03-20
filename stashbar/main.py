import os
os.environ["GDK_BACKEND"] = "x11"

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, GLib
import stash_store

ICONE = {
    "testo": "📝",
    "file":  "📁",
    "link":  "🔗",
    "immagine": "🖼️",
}

LARGHEZZA = 80

class StashBarApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.zenith.stashbar")

    def do_activate(self):
        win = Gtk.ApplicationWindow(application=self)
        win.set_title("StashBar")
        win.set_decorated(False)
        win.set_resizable(False)

        # Sfondo scuro via CSS
        css = Gtk.CssProvider()
        css.load_from_string("window { background-color: #2b2b2b; color: #ffffff; }")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # --- UI ---
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        win.set_child(main_box)

        # Intestazione
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.set_margin_top(12)
        header.set_margin_bottom(8)
        header.set_margin_start(12)
        header.set_margin_end(12)

        titolo = Gtk.Label(label="StashBar")
        titolo.set_hexpand(True)
        titolo.set_xalign(0)
        header.append(titolo)

        btn_svuota = Gtk.Button(label="Svuota")
        btn_svuota.connect("clicked", self._svuota)
        header.append(btn_svuota)

        main_box.append(header)
        main_box.append(Gtk.Separator())

        # Lista elementi con scrollbar
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)

        self.lista = Gtk.ListBox()
        self.lista.set_margin_start(8)
        self.lista.set_margin_end(8)
        self.lista.set_margin_top(8)
        self.lista.set_margin_bottom(8)
        scrolled.set_child(self.lista)
        main_box.append(scrolled)

        self.win = win
        self._setup_drop()
        self._aggiorna_lista()

        # Mostra la finestra e poi applica gli hint X11
        win.present()

        # Aspetta che la finestra sia davvero visibile prima di applicare gli hint
        GLib.idle_add(self._applica_hint_x11)

    def _applica_hint_x11(self):
        """
        Applica gli hint X11 per:
        - tenere la finestra sempre in primo piano
        - toglierla dalla taskbar e dalla dock
        - ancorarla al bordo destro
        """
        display = self.win.get_display()
        surface = self.win.get_surface()

        if surface is None:
            # La finestra non è ancora pronta, riprova al prossimo ciclo
            return True

        # Ottieni le dimensioni dello schermo
        monitor = display.get_monitors()[0]
        geo = monitor.get_geometry()
        altezza = geo.height
        x = geo.x + geo.width - LARGHEZZA
        y = geo.y

        # Ridimensiona e posiziona
        self.win.set_default_size(LARGHEZZA, altezza)

        # Usa xdotool per posizionare e impostare gli hint
        # (più affidabile degli hint GTK su XWayland)
        import subprocess
        
        # Ottieni il window ID
        try:
            result = subprocess.run(
                ["xdotool", "search", "--name", "StashBar"],
                capture_output=True, text=True
            )
            wid = result.stdout.strip().split("\n")[-1]

            if wid:
                # Posiziona a destra
                subprocess.run(["xdotool", "windowmove", wid, str(x), str(y)])
                # Ridimensiona
                subprocess.run(["xdotool", "windowsize", wid, str(LARGHEZZA), str(altezza)])
                # Sempre in primo piano
                subprocess.run(["wmctrl", "-i", "-r", wid, "-b", "add,above"])
                # Togli dalla taskbar
                subprocess.run(["wmctrl", "-i", "-r", wid, "-b", "add,skip_taskbar,skip_pager"])
        except Exception as e:
            print(f"Hint X11 non applicati: {e}")

        return False  # False = non ripetere

    def _aggiorna_lista(self):
        while True:
            riga = self.lista.get_row_at_index(0)
            if riga is None:
                break
            self.lista.remove(riga)

        elementi = stash_store.carica()
        for i, elemento in enumerate(elementi):
            riga = self._crea_riga(elemento, i)
            self.lista.append(riga)

    def _crea_riga(self, elemento, indice):
        riga = Gtk.ListBoxRow()

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box.set_margin_top(6)
        box.set_margin_bottom(6)
        box.set_margin_start(8)
        box.set_margin_end(4)

        icona = Gtk.Label(label=ICONE.get(elemento["tipo"], "?"))
        box.append(icona)

        testo = elemento["contenuto"]
        if len(testo) > 35:
            testo = testo[:35] + "…"
        etichetta = Gtk.Label(label=testo)
        etichetta.set_hexpand(True)
        etichetta.set_xalign(0)
        box.append(etichetta)

        btn_x = Gtk.Button(label="✕")
        btn_x.set_has_frame(False)
        btn_x.connect("clicked", lambda _, idx=indice: self._rimuovi(idx))
        box.append(btn_x)

        riga.set_child(box)

        # Drag-out verso altre app
        drag_source = Gtk.DragSource.new()
        drag_source.set_actions(Gdk.DragAction.COPY)
        contenuto = elemento["contenuto"]

        def on_prepare(source, x, y, c=contenuto):
            return Gdk.ContentProvider.new_for_value(c)

        drag_source.connect("prepare", on_prepare)
        riga.add_controller(drag_source)

        return riga

    def _setup_drop(self):
        # Drop target 1 — file dal file manager
        drop_file = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)

        def on_drop_file(target, valore, x, y):
            for gfile in valore.get_files():
                percorso = gfile.get_path()
                if percorso:
                    stash_store.aggiungi(percorso, "file")
            self._aggiorna_lista()
            return True

        drop_file.connect("drop", on_drop_file)
        self.lista.add_controller(drop_file)

        # Drop target 2 — testo e link
        drop_testo = Gtk.DropTarget.new(str, Gdk.DragAction.COPY)

        def on_drop_testo(target, valore, x, y):
            contenuto = str(valore).strip()
            if not contenuto:
                return False
            if contenuto.startswith("http://") or contenuto.startswith("https://"):
                tipo = "link"
            else:
                tipo = "testo"
            stash_store.aggiungi(contenuto, tipo)
            self._aggiorna_lista()
            return True

        drop_testo.connect("drop", on_drop_testo)
        self.lista.add_controller(drop_testo)

    def _rimuovi(self, indice):
        stash_store.rimuovi(indice)
        self._aggiorna_lista()

    def _svuota(self, _):
        stash_store.salva([])
        self._aggiorna_lista()

app = StashBarApp()
app.run()
