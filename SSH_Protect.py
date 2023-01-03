import paramiko
import subprocess

# Connect to the Debian machine via SSH
ssh = paramiko.SSHClient()
ssh.connect('debian.example.com', username='user', password='password')

# Search the auth.log file for failed login attempts
_, stdout, _ = ssh.exec_command('grep "sshd.*Failed password" /var/log/auth.log')
failed_logins = stdout.read().strip().split('\n')

# Extract the IP addresses of the clients and drop their traffic
for login in failed_logins:
    ip = login.split()[-3][1:-1]  # extract IP address from log entry
    subprocess.run(['iptables', '-I', 'INPUT', '-s', ip, '-j', 'DROP'])

# Close the SSH connection
ssh.close()
