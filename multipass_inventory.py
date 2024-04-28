#!/usr/bin/env python3
import json
import subprocess
import re

def update_hosts_file(hosts_info):
    hosts_file_path = '/etc/hosts'
    start_marker = '# -- Start Multipass Managed Hosts --\n'
    end_marker = '# -- End Multipass Managed Hosts --\n'

    # Read the current hosts file
    with open(hosts_file_path, 'r') as file:
        lines = file.readlines()

    # Check if the markers are present
    start_exists = any(start_marker in line for line in lines)
    end_exists = any(end_marker in line for line in lines)

    # Remove old Multipass entries between markers
    if start_exists and end_exists:
        start_index = lines.index(start_marker)
        end_index = lines.index(end_marker)
        del lines[start_index + 1:end_index]

    # If the markers are not present, append them
    elif not start_exists and not end_exists:
        lines.append(start_marker)
        lines.append(end_marker)
        start_index = lines.index(start_marker)
        end_index = lines.index(end_marker)

    # Insert new Multipass entries
    new_entries = [f"{info['ip']} {info['name']}\n" for info in hosts_info]
    lines[start_index + 1:start_index + 1] = new_entries

    # Write back to the hosts file
    with open(hosts_file_path, 'w') as file:
        file.writelines(lines)

def main():
    output = subprocess.run(['multipass', 'list', '--format=json'], capture_output=True)
    vms = json.loads(output.stdout)

    inventory = {'all': {'hosts': []}}
    hosts_info = []

    for vm in vms['list']:
        if vm['state'] == 'Running':
            vm_name = vm['name']
            vm_ip = vm['ipv4'][0] if vm['ipv4'] else '127.0.0.1'  # Default IP if none assigned
            inventory['all']['hosts'].append(vm_name)
            hosts_info.append({'name': vm_name, 'ip': vm_ip})

    # Update /etc/hosts with current VM info
    update_hosts_file(hosts_info)

    # Output inventory in JSON format
    print(json.dumps(inventory))

if __name__ == '__main__':
    main()
