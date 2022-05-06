from easyddns.domain.synchronizes.records import IPv4AdressPolicy


def test_recognize_ipv4():
    context = "dfagdasdfa1.23.412.1"
    idenitfy = IPv4AdressPolicy()
    result = idenitfy.ipv4(context)
    print(result)
