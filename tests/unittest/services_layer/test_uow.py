from easyddns.service_layer.services import get_sync_status, register_sychronizer
from easyddns.service_layer.unit_of_work import DnspodUnitOfWork
from easyddns.service_layer.sessions import DnspodSession


def test_get_sync_status():
    sync = register_sychronizer(
        user_id="89873",
        token="d4a48203516889f91940a55626807361",
        domain="aoitech.cn",
        subdomain="www",
    )

    uow = DnspodUnitOfWork(DnspodSession, 3, 3, print)
    status = get_sync_status(sync, uow)
    print(status)
