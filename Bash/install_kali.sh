#!/bin/bash

##########################################
## Atualiza pacotes instalados
sudo apt-get update
sudo apt-get upgrade


##########################################
## Instala pacotes utilizados

# Pacotes head do kernel atual
sudo apt-get install -y linux-headers-$(uname -r)

# Pacotes de desenvolvimento
sudo apt-get install -y libc6 gcc g++ pip pip3 clinfo pkg-config g++-multilib libc6-dev-i386 autoconf openssl libssl-dev pwntools python python3

# Outras ferramentas
sudo apt-get install -y hashcat-utils hashcat deepin-screenshot keepassx netcat-traditional

# Atualiza o sistema para usar no NC tradicional ao invés do que vem no Kali
sudo rm /etc/alternatives/nc && sudo ln -s /bin/nc.traditional /etc/alternatives/nc


##########################################
## Adiciona o Alias para tail
echo "Criando alias para tailf"
if [ "$(id -u)" != "0" ]; then
    alias tailf="tail -f" >> ~/.bashrc
fi
alias tailf="tail -f" >> /root/.bashrc

##########################################
## Habilita serviço de SSH
systemctl enable ssh.service

##########################################
## Instala o peda no GDB
if [ "$(id -u)" != "0" ]; then
    git clone https://github.com/longld/peda.git ~/peda
    echo "source ~/peda/peda.py" >> ~/.gdbinit
fi
git clone https://github.com/longld/peda.git /root/peda
echo "source /root/peda/peda.py" >> /root/.gdbinit

