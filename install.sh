#!/bin/bash

echo "Installazione Zenith..."

# Clona la repo se non c'è già
if [ ! -d ~/zenith ]; then
  git clone https://github.com/ZenithDevss/zenith ~/zenith
fi

#---------------------------------
# --> Installazione Componenti <--
#---------------------------------
# Neovim + dipendenze
sudo apt install -y gcc curl
sudo snap install nvim --classic
# Fastfetch
sudo add-apt-repository ppa:zhangsongcui3371/fastfetch -y
sudo apt update
sudo apt install -y fastfetch

# Crea link simbolico per configurazioni varie
[ ! -L ~/.config/nvim ] && ln -s ~/zenith/nvim ~/.config/nvim
[ ! -L ~/.config/fastfetch ] && ln -s ~/zenith/fastfetch ~/.config/fastfetch
# Controlla che il file welcome non sia in .bashrc e lo aggiunge
grep -q "welcome.sh" ~/.bashrc || echo "bash ~/zenith/welcome.sh" >>~/.bashrc

# --- StashBar ---
echo "Installazione StashBar..."

# Dipendenze
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-4.0 xdotool wmctrl

# Autostart: crea il file .desktop se non esiste già
mkdir -p ~/.config/autostart
if [ ! -f ~/.config/autostart/stashbar.desktop ]; then
  cat > ~/.config/autostart/stashbar.desktop << EOF
[Desktop Entry]
Type=Application
Name=StashBar
Comment=Zenith sidebar drag and drop
Exec=/usr/bin/python3 $HOME/zenith/stashbar/main.py
Hidden=false
X-GNOME-Autostart-enabled=true
EOF
  echo "Autostart configurato."
else
  echo "Autostart già configurato, salto."
fi

echo "Fatto!"
