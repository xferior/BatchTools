# Script to build test file for use with AnsibleBatchGen.py

import sys
import random

def distribute_hosts(total_batches, total_hosts):
  
    # Calculate the average number of hosts per batch
    avg_hosts_per_batch = total_hosts // total_batches
    
    # Initialize distribution with each batch having the average number
    distribution = [avg_hosts_per_batch] * total_batches
    
    # Calculate how many hosts are still left to be distributed
    remaining_hosts = total_hosts - sum(distribution)

    # Evenly distribute the remaining hosts across the batches
    for i in range(remaining_hosts):
        distribution[i % total_batches] += 1

    # Diversity distribution
    for i in range(total_batches):
        if distribution[i] > 1:
    
            # Randomly decide to add or subtract a host from the batch
            change = random.randint(-1, 1)
            distribution[i] += change
            
            # Adjust another batch to balance the change and maintain total hosts
            adjust_index = (i + random.randint(1, total_batches - 1)) % total_batches
            distribution[adjust_index] -= change

    return distribution

def write_to_file(total_batches, distribution, filename):
    
    # Write the distribution to a file
    with open(filename, 'w') as file:
        for i in range(total_batches):
    
            # Format the batch number as B001, B002, etc.
            batch_number = f"B{str(i + 1).zfill(3)}"
            
            # Write batch number and host count to the file
            file.write(f"{batch_number},{distribution[i]}\n")

def is_number(s):
    
    # Check if the string 's' is an integer
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    
    # Check for the correct number of arguments and ensure they are only numbers
    if len(sys.argv) != 4 or not all(is_number(arg) for arg in sys.argv[1:]):
        print("Usage: python script.py <total_batches> <total_hosts> <output_file_number>")
        sys.exit(1)

    # Parse arguments
    total_batches = int(sys.argv[1])
    total_hosts = int(sys.argv[2])
    output_file_number = sys.argv[3]
    
    # Set the output filename
    output_filename = f"/tmp/numbers_{output_file_number}"

    # Generate the distribution
    distribution = distribute_hosts(total_batches, total_hosts)
   
    # Write the distribution to file
    write_to_file(total_batches, distribution, output_filename)
