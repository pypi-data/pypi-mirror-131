import ipaddress
import logging
import re
import socket

# Default module logger

logger = logging.getLogger("iupy/network")


# Host Utilities

def get_my_ip(destination=None, **kwargs):
    """
    This function returns a string which contains the host's source IP address for connections to a given destination.
    In the absensce of a destination, well-know address of 4.2.2.1 will be used to make the determination.

    The function uses the dual-stack AF_INET6 family by default.  A value of None will be returned if a valid IP
    address cannot be determined.

    The only allowable optional keyword is version, which should be either 4 or 6, which have the following effects:

    * Specifying version 4 will use the AF_INET socket only, returning IPv4 addresses only.
    * Specifying version 6 will use return any IPv4 address as IPv6 masked format.

    :param destination:
    :param kwargs:
    :return:
    """

    logger = logging.getLogger("iupy/network/get_my_ip")

    # Only do an IPv4 socket if specified, otherwise leverage dual-stack.

    if kwargs.get('version', 0) == 4:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    # Specify the destination as well-known 4.2.2.1 if no value is specified:

    if destination:
        test_ip = destination
    else:
        test_ip = "4.2.2.1"

    # Open our socket to the specified destination.

    try:
        s.connect((test_ip, 1))
        my_ip = ipaddress.ip_address(s.getsockname()[0])
    except socket.error as error_message:
        logger.debug("Socket error for {} / {}".format(test_ip, error_message))
        my_ip = None
    finally:
        s.close()

    # Return None from the previous socket error.

    if not my_ip:
        return None

    # If this is IPv6, check and see if we have a mapped IPv4 object.
    # Convert this to an IPv4 address if version 6 was not explicitly specified.

    if my_ip.version == 6:
        if my_ip.ipv4_mapped and kwargs.get('version', 0) != 6:
            my_ip = ipaddress.IPv4Address(int(ipaddress.ip_address(str(my_ip).replace('::ffff:', '::'))))

    logger.debug("Source address to reach {} is {}.".format(test_ip, my_ip))

    return str(my_ip)


# ACL Utilities

def v4_bits_to_mask(v4_bitlength):
    """
    Returns an IPv4 Netmask based upon a number of bits from 0-32.

    Returns None if the mask source is not in range or is otherwise invalid.

    :param v4_bitlength:
    :return:
    """

    logger = logging.getLogger("iupy/network/v4_bits_to_mask")

    # Return the netamsk, value if the format is valid.

    try:
        netmask = str(ipaddress.IPv4Network(("0.0.0.0/{}").format(v4_bitlength)).netmask)
        logger.debug("Netmask for {} is {}".format(v4_bitlength, netmask))

    except ipaddress.NetmaskValueError as error_message:
        netmask = None
        logger.debug("{}".format(error_message))

    return netmask


def v4_mask_to_bits(v4_mask):
    """
    This function takes in a netmask and returns the proper consecutive bitwise value.

    This only counts the bits from left to right until the first 0 is reached.  For example, a submitted mask
    of 255.255.0.255 will return a bit value of 16, and not 24.

    The function returns None if the mask does not meet the IPv4 Regex.

    :param v4_mask:
    :return:
    """

    logger = logging.getLogger("iupy/network/v4_mask_to_bits")

    # Get the bits out of a valid netmask, else return None.

    try:
        bit_value = ipaddress.IPv4Network(("0.0.0.0/{}").format(v4_mask)).prefixlen
        logger.debug("Bits in {} is {}".format(v4_mask, bit_value))

    except ipaddress.NetmaskValueError as error_message:
        bit_value = None
        logger.debug("{}".format(error_message))

    return bit_value


def v4_wildcard(v4_mask):
    """
    This function returns a wildcard mask based upon either a valid bit length or IP Address.  This is different than
    a hostmask provided by the ipaddress library, because wildcard mask does not need to have consecutive bits.

    A bit length will be converted into a netmask first.

    :param v4_mask:
    :return:
    """

    logger = logging.getLogger("iupy/network/v4_wildcard")

    bitbox = ''

    # If we have a numeric between 0-32, get the netmask value.

    if re.search(r'^([0-9]|[12][0-9]|3[0-2])$', str(v4_mask)):
        v4_mask = v4_bits_to_mask(v4_mask)

    # Verify the netmask meets a strict IPv4 format.

    if re.search(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                 str(v4_mask)):

        # Convert the integer value of the address into bits, stripping out the "0b" binary indicator.

        bitbox = str(bin(int(ipaddress.ip_address(v4_mask)))).replace('0b', '')

        # Fill the full value out to 32 bits, if necessary.
        filler = ''

        for i in range(len(bitbox), 32):
            filler += "0"

        bitbox = filler + bitbox

    # If the bitbox is empty, then we did not have a valid source.  Return None.

    if bitbox == '':
        logger.debug("Invalid wildcard source: {}".format(v4_mask))
        return None

    # Invert all the bits.

    bitflip = ''

    for c in bitbox:
        if c == "1":
            bitflip += "0"
        else:
            bitflip += "1"

    wildcard_mask = str(ipaddress.ip_address(int(bitflip, 2)))

    # Uncomment below to send the bit values to debug
    # logger.debug("Bitbox {} / Bitflip {}".format(bitbox, bitflip))

    logger.debug("Wildcard for {} is {}".format(v4_mask, wildcard_mask))

    return wildcard_mask
