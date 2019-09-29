#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo "Please, run this script as root"
    exit 1
fi

##########################################
## Atualiza pacotes instalados
apt-get update && apt-get upgrade

##########################################
## Recomendado atualizar todo o sistema
#apt update && apt full-upgrade

##########################################
## Instala pacotes utilizados

# Pacotes head do kernel atual
apt-get install -y linux-headers-$(uname -r)

# Pacotes de desenvolvimento
apt-get install -y libc6 gcc g++ pip pip3 clinfo pkg-config g++-multilib libc6-dev-i386 autoconf openssl libssl-dev pwntools python python3 gcc-6-multilib gcc-multilib

# Outras ferramentas
apt-get install -y hashcat-utils hashcat deepin-screenshot keepassx netcat-traditional
pip install --upgrade pip
pip install --upgrade pwntools
pip install --upgrade libformatstr
pip install --upgrade ropper
pip install --upgrade ropgadget

# Atualiza o sistema para usar no NC tradicional ao invés do que vem no Kali
rm /etc/alternatives/nc && ln -s /bin/nc.traditional /etc/alternatives/nc


##########################################
## Adiciona o Alias para tail
echo "Criando alias para tailf"
if [ "$(grep 'alias tailf' /root/.bash_aliases 2>/dev/null | wc -l)" -eq "0" ]; then
    echo 'alias tailf="tail -f"' >> /root/.bash_aliases
	echo 'alias ll="ls -lah"' >> /root/.bash_aliases
fi

##########################################
## Habilita serviço de SSH
systemctl enable ssh.service

##########################################
## Instala o peda no GDB
if [ "$(grep 'peda.py' /root/.gdbinit 2>/dev/null | wc -l)" -eq "0" ]; then
    git clone https://github.com/longld/peda.git /opt/peda
    echo "source /opt/peda/peda.py" >> /root/.gdbinit
    echo "set follow-fork-mode parent" >> /root/.gdbinit
fi


############
## Processos de usuários

for u in $(getent passwd | cut -d: -f1); do
    if [ -d "/home/$u" ]; then
        echo "Path found to user $u"
        
        ##########################################
        ## Adiciona o Alias para tail
        echo "Criando alias para tailf"
        if [ "$(grep 'alias tailf' /home/$u/.bash_aliases 2>/dev/null | wc -l)" -eq "0" ]; then
            echo 'alias tailf="tail -f"' >> /home/$u/.bash_aliases
			echo 'alias ll="ls -lah"' >> /home/$u/.bash_aliases
        fi
        
        ##########################################
        ## Instala o peda no GDB
        if [ "$(grep 'peda.py' /home/$u/.gdbinit 2>/dev/null | wc -l)" -eq "0" ]; then
            echo "source /opt/peda/peda.py" >> /home/$u/.gdbinit
	    echo "set follow-fork-mode parent" >> /home/$u/.gdbinit
        fi
        
    fi
done


