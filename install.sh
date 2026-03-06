#!/bin/bash

echo "Installazione Zenith..."

# Clona la repo se non c'è già
if [ ! -d ~/zenith ]; then
  git clone https://github.com/ZenithDevss/zenith ~/zenith
fi

# Installazione componenti Zenith
sudo snap install nvim --classic

# Crea link simbolico per configurazione neovim
ln -s ~/zenith/nvim ~/.config/nvim

echo "bash ~/zenith/welcome.sh" >> ~/.bashrc

echo "Fatto!"
