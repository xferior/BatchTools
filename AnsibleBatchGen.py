import sys
import os

# Read and parse batches from a file
def read_batches(file_path):

    # Check if the file exists
    if not os.path.exists(file_path):
        print_error(f"File '{file_path}' not found.")

    # Return a list of tuples (BatchID, NumberOfHosts), excluding batches with 0 hosts
    with open(file_path, 'r') as file:
        return [(line.split(',')[0], int(line.split(',')[1])) for line in file if int(line.split(',')[1]) > 0]

# Read the scheduled start time from a file
def read_start_time(ct, time_file_path):

    # Check if the file exists
    if not os.path.exists(time_file_path):
        print_error(f"File '{time_file_path}' not found.")

    # Return the start time if the CT value is found
    with open(time_file_path, 'r') as file:
        for line in file:
            if line.startswith(ct):
                return line.strip().split(',')[1]

    # Print error if CT value is not found
    print_error(f"CT value '{ct}' not found in '{time_file_path}'.")

# Read the list of enabled NODEs from a file
def read_enabled_nodes(file_path):
    try:
    
        # Parse NODE numbers, ensuring they follow the expected format
        with open(file_path, 'r') as file:
            nodes = [int(line.strip()[4:]) for line in file if line.strip().startswith("NODE") and line.strip()[4:].isdigit()]
            if not nodes:
                raise ValueError("No enabled NODEs found.")
            return nodes
    except FileNotFoundError:
        print_error(f"File '{file_path}' not found.")

# Distribute batches among enabled NODEs
def distribute_batches(batches, enabled_nodes):

    # Initialize a dictionary for NODEs with empty batches and zero hosts
    nodes = {node: {'batches': [], 'total_hosts': 0} for node in enabled_nodes}
    for batch, hosts in sorted(batches, key=lambda x: x[1], reverse=True):
    
        # Find the NODE with the least total hosts and assign the batch to it
        least_loaded_node = min(nodes, key=lambda x: (nodes[x]['total_hosts'], len(nodes[x]['batches'])))
        nodes[least_loaded_node]['batches'].append(batch)
        nodes[least_loaded_node]['total_hosts'] += hosts
    return nodes

# Create a Bash script based on distributed batches
def create_bash_script(distributed_nodes, start_time, ct):
    total_hosts = sum(node_info['total_hosts'] for node_info in distributed_nodes.values())

    bash_script = "#!/bin/bash\n\n"
    bash_script += "TZ='America/Los_Angeles'\n"
    bash_script += "start_time=$(date -d '{} today' +%s)\n".format(start_time)
    bash_script += "current_time=$(date +%s)\n"
    bash_script += "if [[ $current_time -lt $start_time ]]; then\n"
    bash_script += "    time_until=$(($start_time - $current_time))\n"
    bash_script += "    echo 'Scheduled start time: {}.'\n".format(start_time)
    bash_script += "    echo -n 'Time until start: '\n"
    bash_script += "    echo $(date -u -d @$time_until +%H:%M:%S)\n"
    bash_script += "    echo ''\n"
    bash_script += "    exit 1\n"
    bash_script += "fi\n\n"
    bash_script += 'echo "****************************************"\n'
    bash_script += 'echo "            ex uno plures"\n'
    bash_script += 'echo "****************************************"\n'
    bash_script += f'echo "Executing {ct} with {total_hosts} hosts."\n\n'
    bash_script += 'echo "\nDo you want to proceed? (yes/no) "\n'
    bash_script += 'read choice\n'
    bash_script += 'if [[ $choice != "yes" ]]; then\n'
    bash_script += '    echo "Exiting"\n'
    bash_script += '    exit 1\n'
    bash_script += 'fi\n\n'
    bash_script += "AA=\"/home/user/aa.sh\"\n"
    for node_num, node_info in distributed_nodes.items():
        if node_info['total_hosts'] == 0:
            continue  # Skip nodes with 0 hosts
        command_list = [f"$AA {ct}{batch}" for batch in node_info['batches']]
        commands = "; ".join(command_list)
        bash_script += (f'ssh $NODE{node_num} "{commands}; '
                       f'echo \'NODE{node_num} job completed!\'" &\n')
    
    bash_script += "\nwait\n"
    bash_script += "chmod -x $0\n"
    bash_script += f'echo "All batches for {ct} completed!"\n'
    bash_script += "exit 0\n"
    return bash_script

# Print an error message and the usage information
def print_error(error_message):
    print("Error:", error_message)
    print_usage()
    sys.exit(1)

# Print usage information
def print_usage():
    print("\nUsage: python3 script.py <CT> [--no-script]")
    print("<CT>: Ticket ID")
    print("--no-script: Optional argument to print NODE information without generating script.\n")
    print("Required files in /tmp directory:")
    print("  1. /tmp/numbers_<CT>: Contains batches with host requirements.")
    print("     Example: B001,12")
    print("  2. /tmp/todays_crq_dates.txt: Scheduled start times for CTs.")
    print("     Example: 123456789,18:00")
    print("  3. /tmp/enable.node: Lists enabled NODEs for batch distribution.")
    print("     Example: NODE1")

# Main function to execute the script
def main():

    # Check if the correct number of arguments is provided
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Argument error:")
        print_usage() 
        sys.exit(1)

    # Set CT value from the arguments
    ct = sys.argv[1]

    # Check if --no-script argument is found
    no_script = len(sys.argv) == 3 and sys.argv[2] == '--no-script'

    # Define file paths for required input files
    file_path = f"/tmp/numbers_{ct}"
    time_file_path = "/tmp/todays_crq_dates.txt"

    # Read and process batches, start time, and enabled nodes
    batches = read_batches(file_path)
    start_time = read_start_time(ct, time_file_path)
    enabled_nodes = read_enabled_nodes("/tmp/enable.node")

    # Distribute batches among the enabled nodes
    distributed_nodes = distribute_batches(batches, enabled_nodes)

    # If the --no-script argument is found, print NODE information only
    if no_script:
        for node_num, node_info in distributed_nodes.items():
            if node_info['total_hosts'] == 0:
                continue  # Skip nodes with no hosts assigned
            batch_list = ' '.join(node_info['batches'])
            total_hosts = node_info['total_hosts']
            print(f"NODE{node_num} @ {batch_list} @ {total_hosts}")
    else:
    
        # Check if /tmp/RUN is a directory and writable
        output_directory = "/tmp/RUN/"
        if not os.path.isdir(output_directory):
            print_error(f"Directory '{output_directory}' does not exist.")
        if not os.access(output_directory, os.W_OK):
            print_error(f"Directory '{output_directory}' is not writable.")

        # Generate and save the script to execute the distribution
        output_file_name = f"start_{ct}.sh"
        output_path = os.path.join(output_directory, output_file_name)
        bash_script = create_bash_script(distributed_nodes, start_time, ct)

        with open(output_path, "w") as file:
            file.write(bash_script)
        os.chmod(output_path, 0o700)
        print(f"Script generated as '{output_path}'.")

if __name__ == "__main__":
    main()
