from easyddns.adapters.ipv4proxy import IPv4Proxy, get_headers
from easyddns.domain.synchronizes.records import IPv4AdressPolicy
from performance import Timer


websites = {
    "https://ipv4.ddnspod.com",
    "http://ip.42.pl/raw",
    "https://myip.ipip.net",
    "https://ddns.oray.com/checkip",
    "https://api-ipv4.ip.sb/ip",
    "https://api.ip.sb/ip",
    "http://ip.3322.net",
    "http://ip.qaros.com",
    "http://ip.cip.cc",
    "http://ident.me",
    "http://icanhazip.com",
    "https://api.ipify.org",
}



def test_query_a_ip_website():
    target = "http://ip.3322.net"

    ip_query = IPv4Proxy()
    print(ip_query.query(target))


def test_get_method_performance():
    target = r"http://ip.3322.net"
    tit = Timer("test")
    headers = get_headers()
    query = IPv4Proxy()
    for _ in range(40):
        tit.start()
        answer = query.get_method(target, headers)
        tit.stop()
        assert IPv4AdressPolicy().is_allowed(answer.text) is True


def test_get_ip_performance_many_websites():
    tit = Timer()
    query = IPv4Proxy()
    fetch = IPv4AdressPolicy()

    tit.start()
    for target in websites:
        headers = get_headers()
        answer = query.get_method(target, headers, 2)
        ip = fetch.ipv4(answer.text)
        if IPv4AdressPolicy().is_allowed(ip):
            break
    tit.stop()


def test_query_ip_performance_many_websites():
    finder = IPv4Proxy()
    tit = Timer()
    url, ans = None, None

    tit.start()
    for target in websites:
        url, ans = finder.query(target)
        if IPv4AdressPolicy().is_allowed(ans):
            break
    tit.stop()
    print(url, ans)


def test_check_access_network():
    finder = IPv4Proxy()
    print(finder.check_access())
