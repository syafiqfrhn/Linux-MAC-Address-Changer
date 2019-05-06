#!/usr/bin/env python

import subprocess
import optparse
import re


# For getting the program's option specified by user. Then the value will be arguments for "change_mac" function.
def get_options():
    # Create an option instance.
    parser = optparse.OptionParser()
    # For users to specify which network interface to be change.
    parser.add_option("-i", "--interface", dest="selected_interface", help="The interface where MAC address will be change.")
    # For users to specify the new MAC address.
    parser.add_option("-m", "--mac", dest="new_mac", help="The new MAC address.")
    # Assign the specified option and argument (not used) into two variables.
    (specified_options, arguments) = parser.parse_args()
    # Check if users specify the option; network interface and a new MAC address.
    if not specified_options.selected_interface:
        parser.error("Please specify a network interface. Use --help for more info.")
    elif not specified_options.new_mac:
        parser.error("Please specify a new MAC address. Use --help for more info.")
    # Return the value of the specified options only if all is specified.
    return specified_options


# For changing MAC address based on the specified option got from "get_options" function.
def change_mac(selected_interface, new_mac):
    # Print a statement as a verification and information.
    print("Changing MAC address for " + selected_interface + " to " + new_mac)
    # Execute a set of Linux commands to change MAC address.
    subprocess.call(["ifconfig", selected_interface, "down"])
    subprocess.call(["ifconfig", selected_interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", selected_interface, "up"])


# For getting the current MAC address.
def get_current_mac (selected_interface):
    # Get and assign the output of the command.
    result_ifconfig = subprocess.check_output(["ifconfig", selected_interface])
    # Filter the "ifconfig" command output using Regex, to only get MAC address.
    result_mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result_ifconfig)
    # Check if the MAC address is found.
    if result_mac_address_search:
        # Return the MAC address found. The "0" group is the first and the only result found.
        return result_mac_address_search.group(0)
    else:
        print("Could not read any MAC address from the network interface.")


# Assign the value returned from "get_options" function.
specified_options = get_options()
# Assign and print the current MAC address of the specified interface.
current_mac = get_current_mac(specified_options.selected_interface)
print("Current MAC address = " + str(current_mac))

# Change the MAC address.
change_mac(specified_options.selected_interface, specified_options.new_mac)

# Assign the newly changed MAC address as current MAC address.
current_mac = get_current_mac(specified_options.selected_interface)
# Check if the newly changed MAC address is equal to the current MAC address.
if current_mac == specified_options.new_mac:
    print("MAC address was successfully changed to " + current_mac)
else:
    print("MAC address did not get changed.")