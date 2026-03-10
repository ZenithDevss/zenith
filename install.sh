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

echo "Fatto!"
