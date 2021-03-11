import unittest

from constants import BASE1, BASE2
from ping import start_pinging, parse_results, skip_address, find_differences


class MyTestCases(unittest.TestCase):
    """Implementation of three test cases which will cover every function
    written in the ping.py script. Primarily testing the connection and
    then if the parsing of the ip addressess is done correctly."""

    def test_connection(self):
        """Ping two well-known sites like Google and Yahoo just to verify the
        ping command is working as expected in your distribution.
        """
        ip_addresses = ["google.com", "yahoo.com"]
        result = start_pinging(ip_addresses)

        results = parse_results(result)
        for website in results:
            self.assertEqual(results[website], 0, "Unsuccessful ping to " +
                             website + ", please review your connection.")

    def test_skip(self):
        """Given a small list of ip addresses and a list of octets, verify if
        they are being correctly removed from the original list.
        """
        skippers = ['1', '3', '4', '5', '8', '10']
        original_list = [BASE1 + "{}".format(i) for i in range(0, 11)] + \
                        [BASE2 + "{}".format(i) for i in range(0, 11)]
        final_list = [BASE1 + "{}".format(i) for i in [0, 2, 6, 7, 9]] + \
                     [BASE2 + "{}".format(i) for i in [0, 2, 6, 7, 9]]

        result_list = skip_address(skippers, original_list)
        self.assertEqual(result_list, final_list)

    def test_find_differences(self):
        """Given a dictionary with ip addresses as keys and the result of
        pinging them as values. Verify which pair of them have different values
        Example For example: '192.168.1.55':0 vs '192.168.2.55':1
        """
        sample_list1 = {BASE1 + "{}".format(i): 0 for i in range(0, 11)}
        sample_list2 = {BASE2 + "{}".format(i): 0 for i in range(0, 11)}
        sample_list1.update(sample_list2)

        sample_list1[BASE1 + "2"] = 1
        sample_list1[BASE2 + "4"] = 1
        sample_list1[BASE2 + "5"] = 1

        final_octet = ['2', '4', '5']
        result_octet = find_differences(sample_list1)
        self.assertEqual(result_octet, final_octet)


if __name__ == '__main__':
    unittest.main()
