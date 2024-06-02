import os
import paramiko
from scp import SCPClient
from datetime import datetime

# Configuration
local_directory = "/path/to/local/directory"
remote_directory = "/path/to/remote/directory"
hostname = "remote.server.com"
port = 22
username = "your_actual_username"  # Replace with your actual username
key_path = "/home/your_username/.ssh/id_rsa"  # Replace with the path to your SSH private key

def create_ssh_client(server, port, user, key_path):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, key_filename=key_path)
    return client

def backup_directory(local_dir, remote_dir):
    try:
        ssh = create_ssh_client(hostname, port, username, key_path)
        scp = SCPClient(ssh.get_transport())

        print(f"Starting backup of {local_dir} to {hostname}:{remote_dir}")
        scp.put(local_dir, remote_path=remote_dir, recursive=True)
        print("Backup completed successfully.")

        scp.close()
        ssh.close()
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

def generate_report(success):
    report_dir = "./backup_reports"
    os.makedirs(report_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"backup_report_{timestamp}.txt")

    with open(report_file, 'w') as f:
        if success:
            f.write(f"Backup of {local_directory} to {hostname}:{remote_directory} completed successfully at {timestamp}.\n")
        else:
            f.write(f"Backup of {local_directory} to {hostname}:{remote_directory} failed at {timestamp}.\n")

    print(f"Report generated: {report_file}")

if __name__ == "__main__":
    backup_success = backup_directory(local_directory, remote_directory)
    generate_report(backup_success)
