#!/bin/bash
 #

 if [ ! -x /sbin/iptables ]; then
 exit 0
 fi


# instala o syslog apt-get install sysklogd
# Adicione a seguinte linha no arquivo rsyslog.conf
# kern.warn -/var/log/iptables.log

# Após dalvar o script em /etc/init.d/firewall executar os comandos abaixo
# chmod 777 /etc/init.d/firewall
# update-rc.d -f firewall defaults

# Comandos
IPTABLES=/sbin/iptables
IFCONFIG=/sbin/ifconfig
ROUTE=/sbin/route
IP=/bin/ip

 start()
 {
 # clear all
 clearall

    # Limpa as regras atuais
    $IPTABLES -F
    $IPTABLES -X
    $IPTABLES -t nat -F
    $IPTABLES -t nat -X
    $IPTABLES -t mangle -F
    $IPTABLES -t mangle -X
    $IPTABLES --flush

    # Regra padrão (Bloqueia tudo)
    $IPTABLES -P INPUT DROP
    $IPTABLES -P OUTPUT DROP
    $IPTABLES -P FORWARD DROP

#   $IPTABLES -A INPUT -j LOG --log-prefix 'INPUT: ' --log-level 4
#   $IPTABLES -A OUTPUT -j LOG --log-prefix 'OUTPUT: ' --log-level 4
#   $IPTABLES -A FORWARD -j LOG --log-prefix 'FORWARD: ' --log-level 4

    $IPTABLES -N LOGDROP > /dev/null 2> /dev/null
    $IPTABLES -F LOGDROP
    $IPTABLES -A LOGDROP -j LOG --log-prefix "LOGDROP: "
    $IPTABLES -A LOGDROP -j DROP

    # Libera os retornos de stados e pacotes de saida
    $IPTABLES -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    $IPTABLES -A OUTPUT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
    $IPTABLES -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

    # Liberando tudo da Loopback
    $IPTABLES -A INPUT -i lo -j ACCEPT

    # Libera forward e adiciona as rotas
    echo 1 > /proc/sys/net/ipv4/ip_forward
    for f in /proc/sys/net/ipv4/conf/*/rp_filter ; do echo 0 > $f ; done
    echo 0 > /proc/sys/net/ipv4/route/flush

    # Indica para rebotar após 1 segundos em caso de kernel panic
    echo 1 > /proc/sys/kernel/panic

    # Carrega módulos para FTP
    modprobe ip_nat_ftp
    modprobe nf_conntrack_ftp
    modprobe ip_conntrack_netlink

    ###############
    # Endereçamento IPs Gerais
    INTERNET=0.0.0.0/0
    MY_NET=192.168.0.1/32

    ###############
    # Grupo: ICMP (icmp-type request = 8, icmp-type response = 0)

    # Libera ICP Request e ICMP Response para todos os escopos
    $IPTABLES -A INPUT -p icmp --icmp-type 0 -s 0/0 -j ACCEPT
    $IPTABLES -A INPUT -p icmp --icmp-type 8 -s 0/0 -j ACCEPT
    $IPTABLES -A OUTPUT -p icmp --icmp-type 0 -j ACCEPT
    $IPTABLES -A OUTPUT -p icmp --icmp-type 8 -j ACCEPT

    
    ###############
    # Internet > Asterisk

    # Libera SSH
    $IPTABLES -A INPUT -s 0/0 -p TCP --sport 1024:65535 --dport 22 -j ACCEPT

    # Libera toda a saída deste server
    $IPTABLES -A OUTPUT -j ACCEPT

    ###############
    # Internet -> Interna

    # Principais Hosts aceitos
    $IPTABLES -A INPUT -s $MY_NET -j ACCEPT
    $IPTABLES -A OUTPUT -o eth+ -j ACCEPT

    

    # Exemplo liberacao
    #$IPTABLES -A INPUT -s 10.10.10.10 -p TCP --dport 80 -j ACCEPT
    #$IPTABLES -A FORWARD -s 0/0 -d 10.10.10.10 -p TCP -m multiport --dports 80,443 -j ACCEPT
            

    #$IPTABLES -t nat -A PREROUTING -s $INTERNET -d 10.10.10.10 -p TCP -m multiport --dports 80 -j DNAT --to-destination 1.1.1.1:8080
    #$IPTABLES -t nat -A POSTROUTING -s 10.10.10.10 -d $INTERNET -j SNAT --to-source 10.10.10.10

    #$IPTABLES -t nat -A POSTROUTING -s $MY_NET -o eth+ -j MASQUERADE

}

 clearall()
 {
    $IPTABLES -F
    $IPTABLES -X
    $IPTABLES -t nat -F
    $IPTABLES -t nat -X
    $IPTABLES -t mangle -F
    $IPTABLES -t mangle -X
    $IPTABLES --flush

    # Regra padrão (Libera tudo)
    $IPTABLES -P INPUT ACCEPT
    $IPTABLES -P OUTPUT ACCEPT
    $IPTABLES -P FORWARD DROP
 }

 case "$1" in
 restart|start)
 start
 ;;
 stop)
 clearall
 ;;
 *)
 echo "Usage: $0 {start|stop|restart}"
 exit 1
 esac

 exit 0


