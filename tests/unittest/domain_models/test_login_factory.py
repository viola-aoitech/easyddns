from easyddns.domain.login.factory import (LoginError, RecordFactory,
                                           UserFactory)
from easyddns.domain.login.record import AliyunUser, DnspodUser


def test_register_user_from_dict():
    data1 = {
        "DNS": {
            "name": "Dnspod",
            "login": {
                "user id": "xx",
                "user token": "xxx"
            }
        },
    }
    data2 = {
        "DNS": {
            "name": "Aliyun",
            "login": {
                'access id': "xx",
                "access key": "xxx"
            }
        },
    }

    data3 = {
        "DNS": {
            "name": "Dnspod",
            "login": {
                'access id': "xx",
                "access key": "xxx"
            }
        },
    }
    try:
        user3 = UserFactory().register(data3)
    except LoginError as er:
        print(er)
    else:
        print(user3)

    user1 = UserFactory().register(data2)
    print(user1)
    assert isinstance(user1, AliyunUser)

    user2 = UserFactory().register(data1)
    print(user2)
    assert isinstance(user2, DnspodUser)


def test_register_record_from_dict():
    data = {
        "Record 2": {
            "type": "AAAA",
            "domain name": "opt.aoitech.cn",
            "ttl": "300"
        },

        "Record 1": {
            "type": "AAAA",
            "domain name": "www.aoitech.cn",
            "ttl": "300"
        },
        "Need 1": {
            "type": "AAAA",
            "domain name": "www.piv3d.com",
            "ttl": "300"
        }
    }
    records = RecordFactory().register_many(data)
    print(records)
