# -*- coding: utf-8 -*-
"""
Created on Thu May 18 15:49:54 2023

@author: EWOLO
"""

import paramiko

# List of IP addresses or hostnames of the client stations
client_stations = ['station1_ip', 'station2_ip', ...]

# SSH credentials
username = 'username'
password = 'password'

# Update commands
update_commands = [
    'choco upgrade all -y',  # Example: using Chocolatey package manager
    # Add more update commands as needed
]

# Log file path
log_file = 'update_log.txt'

def execute_ssh_command(client, command):
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
    output = ssh_stdout.read().decode().strip()
    error = ssh_stderr.read().decode().strip()

    return output, error

def write_log(message):
    with open(log_file, 'a') as f:
        f.write(message + '\n')

# Iterate over each client station and perform updates
for station in client_stations:
    write_log(f'Updating {station}...')

    # SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(station, username=username, password=password)

        # Execute update commands via SSH
        for update_command in update_commands:
            output, error = execute_ssh_command(client, update_command)

            if error:
                write_log(f'Failed: {update_command}')
                write_log(f'Error message: {error}')
            else:
                write_log(f'Success: {update_command}')
    except paramiko.AuthenticationException as e:
        write_log(f'Failed to authenticate for {station}')
        write_log(f'Error message: {str(e)}')
    except paramiko.SSHException as e:
        write_log(f'Failed to establish SSH connection to {station}')
        write_log(f'Error message: {str(e)}')
    finally:
        client.close()

    write_log('-----------------------------------')

write_log('Updates completed.')
