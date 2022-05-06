
from easyddns.configs.websites import IP_WEBSITES
from easyddns.service_layer.services import register_sychronizer
from easyddns.service_layer.sessions import DnspodSession
from easyddns.service_layer.unit_of_work import DnspodUnitOfWork
from performance import Timer


def test_using_session_query_sync():
    sync = register_sychronizer(
        user_id="89873",
        token="d4a48203516889f91940a55626807361",
        domain="aoitech.cn",
        subdomain="www",
    )

    session = DnspodSession()

    itt = Timer()
    itt.start()
    sync = session.query(sync, IP_WEBSITES)
    itt.stop()
    print(sync, sync.version_number)


def test_using_uow_init_a_session():
    sync = register_sychronizer(
        user_id="89873",
        token="d4a48203516889f91940a55626807361",
        domain="aoitech.cn",
        subdomain="www",
    )
    repeats = 3
    timeout = 3
    uow = DnspodUnitOfWork(DnspodSession, repeats, timeout, print)

    with uow:
        dns = uow.query(sync)
        if dns.need_sync():
            dns.sync()
    print(dns)
    assert dns.can_delpoy()
    assert dns.dmz_record.ip == dns.dnspod_record.ip
