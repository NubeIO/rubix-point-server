import ipaddress


def is_ipv4(val: str) -> bool:
    try:
        if val == 'localhost':
            return True
        if ipaddress.IPv4Network(val):
            return True
    except:
        return False


def is_port(port: int) -> bool:
    try:
        if 1 <= port <= 65535:
            return True
    except:
        return False

ip = "0.0.0.0"
print(is_ipv4(ip))

ip = "192.168.0.0"
print(is_ipv4(ip))


port = "0.0.0.0.0"
print(is_port(ip))

port = 508
print(is_port(port))