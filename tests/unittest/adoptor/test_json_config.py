from pathlib import Path
from easyddns.configs.jsonconfig import JsonConfig
from easyddns.domain.login.record import DnspodUser
from easyddns.domain.login.exceptions import LoginError


def test_read_json_from_disk():
    try:
        configs = JsonConfig('tests/data/dnspod_config.json')
        params = configs._read(Path('tests/data/dnspod_config.json'))
    except LoginError as er:
        print(er)
    else:
        print(params)
        assert params['DNS']['name'] == 'Dnspod'
        assert params['DNS']['login']['user id'] == '89873'

        # records = set()
        for keys, items in zip(params.keys(), params.items()):
            if 'Record' in keys:
                print(items)


def test_read_user_from_JsonConfig():
    try:
        config = JsonConfig('tests/data/dnspod_config.json')
        config.read()
    except LoginError as er:
        print(er)
    else:
        print(config)
        assert isinstance(config.user, DnspodUser)
