from easyddns.domain.synchronizes.dnspod import DnspodRecord


def test_register_record():
    record = DnspodRecord.register("aoitech.cn","www", "211.12340.123", "1234")
    assert record.have_ip() is False

    record = DnspodRecord.register("aoitech.cn","www", "2240.123", "1234")
    assert record.have_ip() is False

    record = DnspodRecord.register("aoitech.cn","www", "2.123.340.123", "1234")
    assert record.have_ip() is True

    record = DnspodRecord.register(
        "aoitech.cn", "www", "1.123.340.123", "1234")
    assert record.have_ip() is True


def test_DnspodRecord_have_ip():
    record1 = DnspodRecord.register("1234", "211.123.343.12df", "aoitech.cn")
    assert record1.have_ip() is False

    record2 = DnspodRecord.register(
        "1234", "211.123.34.123df.23", "aoitech.cn"
    )
    assert record2.have_ip() is False

    record3 = DnspodRecord.register("1234", ".123.34.123df.23", "aoitech.cn")
    assert record3.have_ip() is False


def test_dnspod_register():
    dnspod = DnspodRecord.register("", "", "")

    assert dnspod.can_deploy() is False
    assert dnspod.have_ip() is False
    assert dnspod.ip is ""
    assert dnspod.id is ""


def test_queried_dnspod():
    dnspod = DnspodRecord.register("", "", "")
    queried = dnspod.replace("12345", "168.156.3.1")
    assert queried.can_deploy() is True
    assert queried.need_sync() is True

    queried = dnspod.replace("12345", "168.156.3.")
