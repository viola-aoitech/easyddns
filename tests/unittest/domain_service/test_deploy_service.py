from easyddns.domain.deploy import make_dnspod_paramas
from easyddns.domain.synchronizes import dmz, dnspod, synchronizer


def test_make_a_sync_able_paramas():
    good_dmz = dmz.DmzRecord.register("123", "dfgadfw1234", "123.123.123.123")
    good_dnspod = dnspod.DnspodRecord.register(
        "any.com", "123.123.123.123", "1234df"
    )

    sync = synchronizer.register_synchornizer(good_dmz, good_dnspod)

    synced = sync.sync()  # version +1
    print(f"{synced.version_number},{sync.dmz_record}")

    paramas = make_dnspod_paramas(synced)
    print(paramas)


def test_use_case_need_sync():
    """user case 1: init a program and need sync them
    """
    good_dmz = dmz.DmzRecord.register(user_id="123", token="dfgadfw1234")
    good_dnspod = dnspod.DnspodRecord.register(domain="any.com")

    sync = synchronizer.register_synchornizer(good_dmz, good_dnspod)

    queired_public_ip = "192.168.3.1"
    queired_dnspod_ip = "192.168.3.3"

    sync.update_dmz_ip(queired_public_ip)
    sync.update_dnspod(new_ip=queired_dnspod_ip, new_id="123456")

    assert sync.need_sync() is True
    sync.sync()

    assert sync.need_sync() is False
    assert sync.can_delpoy() is True  # not need
    print(
        f"is done sync:{sync._master.ip}-{sync._slaver.ip}-ver:{sync.version_number}")
    assert sync.version_number == 3


def test_use_case_not_need_sync():
    new_dmz = dmz.DmzRecord.register(user_id="123", token="dfgadfw1234")
    new_dnspod = dnspod.DnspodRecord.register(domain="any.com")
    sync = synchronizer.register_synchornizer(new_dmz, new_dnspod)

    queired_public_ip = "192.168.3.1"
    sync.update_dmz_ip(queired_public_ip)

    queired_dnspod_ip = "192.168.3.1"
    sync.update_dnspod(new_ip=queired_dnspod_ip, new_id="123456")

    assert sync.need_sync() is False
    assert sync.can_delpoy() is True  # not need
    print(sync.version_number)
    assert sync.version_number == 2

