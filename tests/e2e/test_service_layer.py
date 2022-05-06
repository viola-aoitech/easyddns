from easyddns.service_layer import services, sessions, unit_of_work
from easyddns.domain.login.record import AliyunUser, DnspodUser
from pathlib import Path


def test_current_path():
    p = Path('.')
    print(p.parent.absolute())


def test_init_app_from_config_file():
    login = services.load_config('./tests/data/dnspod_config.json')
    user = login.user
    records = login.records

    if isinstance(user, DnspodUser):
        for record in records:
            domain = record.domain
            sub_domain = record.sub_domain
            # ttl = record.ttl
            # rtype = record.rtype
            sync = services.register_sychronizer(
                user.usr_id, user.usr_token, domain, sub_domain
            )
            uow = unit_of_work.DnspodUnitOfWork(
                sessions.DnspodSession, 3, 2, print
            )

            result = services.get_sync_status(sync, uow)
            print(result)

    if isinstance(user, AliyunUser):
        raise NotImplementedError
