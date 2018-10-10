#!/bin/bash

##########################################
## Atualiza pacotes instalados
sudo apt-get update && apt-get upgrade

##########################################
## Recomendado atualizar todo o sistema
#apt update && apt full-upgrade

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
    if [ "$(grep 'alias tailf' ~/.bashrc | wc -l)" == "0" ]; then
        echo 'alias tailf="tail -f"' >> ~/.bashrc
    fi
fi
if [ "$(sudo grep 'alias tailf' /root/.bashrc | wc -l)" == "0" ]; then
    sudo echo 'alias tailf="tail -f"' >> /root/.bashrc
fi

##########################################
## Habilita serviço de SSH
sudo systemctl enable ssh.service

##########################################
## Instala o peda no GDB
if [ "$(id -u)" != "0" ]; then
    if [ "$(grep 'peda.py' ~/.gdbinit | wc -l)" == "0" ]; then
        git clone https://github.com/longld/peda.git ~/peda
        echo "source ~/peda/peda.py" >> ~/.gdbinit
    fi
fi
if [ "$(sudo grep 'peda.py' /root/.gdbinit | wc -l)" == "0" ]; then
    sudo git clone https://github.com/longld/peda.git /root/peda
    sudo echo "source /root/peda/peda.py" >> /root/.gdbinit
fi

