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


def pingit(ip):
    try:
        sec = ping(ip, timeout=1)
        if sec:
            print('ping %s in %s ms\n' % (ip, sec * 1000))
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
