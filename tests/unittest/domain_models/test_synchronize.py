from easyddns.domain.synchronizes import dmz, dnspod
from easyddns.domain.synchronizes.synchronizer import register_synchornizer


def test_init_sync():
    init_dmz = dmz.DmzRecord.register("123", "dfgadfw1234")
    init_dnspod = dnspod.DnspodRecord.register("any.com", "", "")

    synchronizer = register_synchornizer(master=init_dmz, slaver=init_dnspod)
    print(synchronizer)

    assert synchronizer.need_sync() is False
    assert synchronizer.can_delpoy() is False

    if (synchronizer.can_delpoy() and synchronizer.can_delpoy()) is False:
        print("we init a new sync,version number is:",
              synchronizer.version_number)

    assert synchronizer.version_number == 0


def test_queried_new_public_ip():
    """测试查询后的业务处理，测试目标：

    同步器聚合根模型业务实现：采用主从方式进行同步，当发现从属得记录与主记录不一致时，采用主
    记录的ipv4地址更新从属记录中的ipv4地址，并将同步后的sync对象部署到 dns 服务器上。

    测试策略，从初始化记录开始，穷举多个情况。以保证业务能够执行完毕。
    """
    # 初始化 dmz 和 dnspod 对象
    init_dmz = dmz.DmzRecord.register("123", "dfgadfw1234")
    init_dnspod = dnspod.DnspodRecord.register("any.com", "", "")
    sync = register_synchornizer(master=init_dmz, slaver=init_dnspod)

    def fake_querier_dmz(dmz: dmz.DmzRecord):
        return dmz.replace(new_ip="192.168.3.1")

    queried_dmz = fake_querier_dmz(init_dmz)
    sync._master = queried_dmz

    assert sync.need_sync() is True  # dnspod have not ipv4 address

    # 读取 dmz 的 ip 后，进行同步。
    def fake_querier_dnspod(dnspod: dnspod.DnspodRecord, new_id="", new_ip=""):
        # don't forget id
        return dnspod.replace(new_ip=new_ip, new_id=new_id)

    queried_dnspod = fake_querier_dnspod(init_dnspod, "1234123", "192.168.3.2")
    sync._master = queried_dmz
    sync._slaver = queried_dnspod
    assert sync.need_sync() is True  # beacause have not id

    # 读取 dmz 的 ip 后，再读取 dnspod 的 ip 后，进行同步。
    queried_dnspod = fake_querier_dnspod(init_dnspod, "1234123", "192.168.3.1")
    sync._master = queried_dmz
    sync._slaver = queried_dnspod
    assert sync.need_sync() is False  # beacause dmz and dnspod have similar ip

    # 读取 dmz 的 ip 后，再读取 dnspod 的 ip 后，再读取dnspod 的 id 后，进行同步。
    queried_dnspod = fake_querier_dnspod(init_dnspod, "1234123", "1.16.3.2")
    sync._master = queried_dmz
    sync._slaver = queried_dnspod
    assert sync.need_sync() is True
    print("prepared for running sync in service layer!", sync)


def test_using_sync_to_processing_new_public_ip():
    # 初始化 dmz 和 dnspod 对象
    init_dmz = dmz.DmzRecord.register("123", "dfgadfw1234")
    init_dnspod = dnspod.DnspodRecord.register("any.com", "", "")
    sync = register_synchornizer(master=init_dmz, slaver=init_dnspod)
    sync.update_dmz_ip(new_ip="192.168.3.1")

    assert sync.version_number == 1
    assert sync.need_sync() is True  # dnspod have not ipv4 address

    sync.update_dnspod("192.168.3.1", "")
    assert sync.version_number == 2
    assert sync.need_sync() is False  # beacause have not id

    sync.update_dnspod("192.168.3.1", "1234")
    assert sync.version_number == 3
    assert sync.need_sync() is False  # beacause dmz and dnspod have similar ip
    assert sync.can_delpoy() is True

    sync.update_dnspod(new_ip="192.168.3.2", new_id="1234")
    assert sync.need_sync() is True
    assert sync.version_number == 4
    # when post-condition has satisfieed the version of sync must greater than 4.
    print(sync)
