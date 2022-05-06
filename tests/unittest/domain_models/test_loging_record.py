from easyddns.domain.login.record import Record


def test_split_domain_name():
    name = "www.aoitech.net"
    print(Record._parser_domain(name))


def test_register_a_record():
    record = Record.register("www.aoitech.cn", 300)
    print(record)
    assert record.domain == 'aoitech.cn'
    assert record.sub_domain == 'www'

    record = Record.register("opt.aoitech.cn", 300)
    print(record)
    assert record.domain == 'aoitech.cn'
    assert record.sub_domain == 'opt'
    assert record.ttl == '300'
