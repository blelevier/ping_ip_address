import multiprocessing
import multiprocessing.dummy
import subprocess
import sys
import time

from constants import BASE1, BASE2

my_dict1 = {}  # Global Variable (TODO: Find a cleaner approach)


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
        ping_reply.returncode (bool): Depending if ping was successful or not
    """
    ping_reply = subprocess.run(["ping", "-c", "2", ip],
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
    if ping_reply.returncode == 0:
        my_dict1[ip] = "Yes"
    else:
        my_dict1[ip] = "No"
    return ping_reply.returncode


def start_pinging(ip):
    """
    Initialize a number of threads (maybe we can run more than this?).
    Implemented using the multiprocessing package, using the basic
    example of data parallellism with Pool.
    Args:
        ip (list): list of ip addresses to be pinged
    """
    num_threads = 15 * multiprocessing.cpu_count()
    p = multiprocessing.dummy.Pool(num_threads)
    p.map(ping, ip)


def find_differences():
    """
    Compare the value in the dictionary to detect which one are different.
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


def test_connection():
    """Ping two well-known sites like Google and Yahoo just to verify the
    ping command is working as expected in your distribution.
    """
    print("************************************************************")
    print("Pinging Google and Yahoo to test connection...")
    ip3 = ["google.com", "yahoo.com"]
    for ip in ip3:
        ping_reply = subprocess.run(["ping", "-c", "2", ip])
        if ping_reply.returncode == 0:
            print("Success pinging " + ip)
        else:
            print("No respone from " + ip + ". Please review your connection.")
    print("************************************************************")


def main():
    start = time.time()
    print("Running...")
    test_connection()

# Create list of ip addresses
    ip_address1 = [BASE1 + "{}".format(i) for i in range(0, 256)]
    ip_address2 = [BASE2 + "{}".format(i) for i in range(0, 256)]
    joint_list_ip = ip_address1 + ip_address2

# Read command line arguments to decide which ip addresses to skip
    if len(sys.argv) > 1:
        to_skip = sys.argv[1:]
        joint_list_ip = skip_address(to_skip, joint_list_ip)

# Start pinging
    start_pinging(joint_list_ip)
    octet_list = find_differences()
    print_final_list(octet_list, my_dict1)

    print("\nRunning time: " + str(time.time() - start) + " seconds")


if __name__ == "__main__":
    main()
