import multiprocessing
import multiprocessing.dummy
import subprocess
import sys
import time

from constants import BASE1, BASE2


def skip_address(skippers, ip):
    """Allow specific IP addresses to be skipped according to user input.
    Args:
        skippers (list): Octets of the ip addresses to be skipped
        ip (list): Original list of ip addresses to be pinged
    Returns:
        ip (list): Original list minus the skipped numbers.
    """
    for number in skippers:
        ip.remove(BASE1 + number)
        ip.remove(BASE2 + number)
    return ip


def ping(ip):
    """Run the console command to ping the ip addresses twice. Output
    from the terminal is not displayed, as there is a lot of information.
    After that, add the ip address to a dict, being the key the ip address
    and the value "Yes" or "No", depending if the connection was successful.
    Args:
        ip (list): list of ip addresses to be pinged
    Return:
         (string): Depending if ping was successful(0) or not(1)
                   Example: '0__192.168.2.239' or '1__192.168.1.80'
                   It will be parsed later.
    """
    ping_reply = subprocess.run(["ping", "-c", "2", ip],
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE) 
    return '{}__{}'.format(ping_reply.returncode, ip)


def start_pinging(ip):
    """Initialize a number of threads (maybe we can run more than this?).
    Implemented using the multiprocessing package, using the basic
    example of data parallellism with Pool.
    Args:
        ip (list): list of ip addresses to be pinged
    Return:
        results (list): Every element will contain the ip pinged and the
                        result. It will be parsed later on and converted
                        into a dict.
    """
    num_threads = 15 * multiprocessing.cpu_count()
    p = multiprocessing.dummy.Pool(num_threads)
    results = p.map(ping, ip)
    return results


def parse_results(results):
    """Parse the ip addresses string list and convert it to a dict with the ip
    address as the key and the value as the result. Example:
    ['0__192.168.2.239', '1__192.168.1.80'] to {'192.168.2.239' : 0,
    '192.168.1.80' : 1}
    Args:
        results (list): list of ip addresses and values to be parsed
    Returns:
        (dict)
    """
    return {result.split('__')[1]: int(result.split('__')[0]) for result
            in results}


def find_differences(my_dict1):
    """
    Compare the value in the dictionary to detect which pings are different.
    For example: '192.168.1.55' vs '192.168.2.55'
    Return:
        octet (list): ip addresses that have different values.
    """
    octet = []
    for i in range(256):
        try:
            if my_dict1[BASE1 + str(i)] != my_dict1[BASE2 + str(i)]:
                octet.append(str(i))
        except KeyError:
            pass

    return octet


def print_final_list(octets, my_dict1):
    """
    Display the final output of the program. In other words, print the
    list of the pair of ip addresses that had different values.
    Args:
        my_dict1 (dict): key=ip address, value= "Yes" or "No"
        octet (list): ip addresses that have different values.
    """
    if not octets:
        print("There were no addresses that were pingable on one range,"
              "but not on another.")
    else:
        print("IP addresses that are pingable on one range, but not on"
              "the other one:")
        for octet in octets:
            print(octet.rjust(3) + " --> " + BASE1 + octet +
                  "\t= " + my_dict1[BASE1 + octet] + ",\t" +
                  BASE2 + octet + "\t= " + my_dict1[BASE2 + octet])


def main():
    start = time.time()
    print("Running...")

# Create list of ip addresses
    joint_list_ip = [BASE1 + "{}".format(i) for i in range(0, 256)] + \
                    [BASE2 + "{}".format(i) for i in range(0, 256)]

# Read command line arguments to decide which ip addresses to skip
    if len(sys.argv) > 1:
        to_skip = sys.argv[1:]
        joint_list_ip = skip_address(to_skip, joint_list_ip)

# Start pinging
    results = start_pinging(joint_list_ip)
# Parse and print results
    ip_results = parse_results(results)
    octets = find_differences(ip_results)
    print_final_list(octets, ip_results)

    print("\nRunning time: " + str(time.time() - start) + " seconds")


if __name__ == "__main__":
    main()
