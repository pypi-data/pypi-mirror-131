# coding: utf-8
import socket
from ping3 import ping
from multiprocessing.dummy import Pool as ThreadPool


def get_ip_sequence(ip):
    prefix = ".".join(ip.split('.')[:-1])
    return ["%s.%s" % (prefix, i) for i in range(2, 254)]


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip


def get_host(ip):
    try:
        return socket.gethostbyaddr(ip)
    except OSError:
        return 'Unknown host'


def sshable(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 22))
            s.close()
            return True
    except Exception as e:
        return False


def pingit(ip):
    try:
        sec = ping(ip, timeout=1)
        if sec:
            host = get_host(ip)
            can_ssh = sshable(ip)
            print('ping %s(%s) in %s ms %s\n' % (ip, host, sec * 1000, " With SSH Enabled" if can_ssh else ""))
    except OSError as e:
        pass
    except Exception as e:
        print('error:%s on ip:%s' % (e, ip))


def main():
    ips = get_ip_sequence(get_host_ip())
    pool = ThreadPool(128)
    pool.map(pingit, ips)


if __name__ == '__main__':
    main()
