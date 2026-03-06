#!/bin/bash

echo "Installazione Zenith..."

# Clona la repo
git clone https://github.com/ZenithDevss/zenith ~/zenith

# Installazione componenti Zenith
sudo snap install nvim --classic

# Crea link simbolico per configurazione neovim
ls -s ~/zenith/nvim ~/.config/nvim

echo "Fatto!"
