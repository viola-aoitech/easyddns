from typing import Dict

from easyddns.adapters.dnsproxy import DnspodProxy
from easyddns.service_layer.services import register_sychronizer


def make_user_params() -> Dict:
    ID = "89873"  # replace with your ID
    Token = "d4a48203516889f91940a55626807361"  # replace with your Token
    return dict(
        login_token=("%s,%s" % (ID, Token)),
        format="json",
        domain="aoitech.cn",  # replace with your domain
        sub_domain="www",  # replace with your sub_domain
        record_type="A",
        record_line="默认",
    )


def test_request_post_to_dnspod_successed():
    login = make_user_params()
    dnspod_service = DnspodProxy()
    r = dnspod_service.post_to_dnspod("https://dnsapi.cn/Record.List",
                                      login, 3
                                      )
    print(r)


def test_request_post_to_dnspod_failed():
    dnspod_service = DnspodProxy()
    r = dnspod_service.post_to_dnspod("adf.wer", {}, 3)
    print(r)
    assert r.status_code is None


def test_using_dnspod_service_query_resolved_ip():
    """_summary_
    """
    params = make_user_params()
    dnspod_service = DnspodProxy()
    answer = dnspod_service.get_record_list(params, timeout=3)
    print(answer)
    # get_record_list(params=params)


def test_dnspod_service_write_ip_failed():
    params = make_user_params()
    dnspod_service = DnspodProxy()
    answer = dnspod_service.write_new_record(params, timeout=3)
    assert answer == "failed"  # beacause hava not ip


def test_dnspod_service_write_a_new_ip_success():
    params = make_user_params()
    dnspod_service = DnspodProxy()
    dnspod_answer = dnspod_service.get_record_list(params, timeout=3)
    print(dnspod_answer)

    params["value"] = dnspod_answer["ip_value"]  # "182.137.54.100"#
    params["record_id"] = dnspod_answer["record_id"]
    print(params)
    dnspod_answer = dnspod_service.write(params, timeout=3)
    assert dnspod_answer == 1


def test_using_dnspod_service_query_sync():
    sync = register_sychronizer(
        user_id="89873",
        token="d4a48203516889f91940a55626807361",
        domain="aoitech.cn",
        subdomain="www",
    )
    dnspod_service = DnspodProxy()
    dnspod_service.set_sync(sync)

    ipv4_address, _ = dnspod_service.query(timeout=10)
    print(ipv4_address)  # ipv4 address


def test_using_dnspod_service_manual_deploy_sync():
    sync = register_sychronizer(
        user_id="89873",
        token="d4a48203516889f91940a55626807361",
        domain="aoitech.cn",
        subdomain="www",
    )

    dnspod_service = DnspodProxy()
    dnspod_service.set_sync(sync)

    old_address, record_id = dnspod_service.query(timeout=10)
    ipv4_address = "192.168.3.1"

    sync.update_dmz_ip(ipv4_address)
    sync.update_dnspod(ipv4_address, record_id)

    dnspod_service.set_sync(sync)
    ans = dnspod_service.delpoy(timeout=10)

    mock_ip, _ = dnspod_service.query(timeout=10)
    assert mock_ip == ipv4_address

    sync.update_dmz_ip(old_address)
    sync.update_dnspod(old_address, record_id)

    dnspod_service.set_sync(sync)
    ans = dnspod_service.delpoy(timeout=10)
    mock_ip, _ = dnspod_service.query(timeout=10)

    print(f"{mock_ip} test result is {ans}")
