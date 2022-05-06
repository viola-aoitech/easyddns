from easyddns.domain.synchronizes.dmz import DmzRecord


def test_dmz_record_register():
    record = DmzRecord.register("89873", "d4a48203516889f91940a55626807361")
    print(record)
    assert "89873" in record.user
    assert "d4a48" in record.user
    assert record.ip == ""


def test_dmz_has_queried():
    record = DmzRecord.register("89873", "d4a48203516889f91940a55626807361")
    assert record.have_ip() is False
    assert record.can_deploy()


def test_dmz_can_sync():
    record = DmzRecord.register("89873", "d4a48203516889f91940a55626807361")
    assert record.need_sync() is False
    assert record.can_deploy() is True

    record = DmzRecord.register(
        "89873", "d4a48203516889f91940a55626807361", "1.16.3.1")
    assert record.need_sync() is True
    assert record.can_deploy() is True


def test_update_new_dmzrecord():
    record = DmzRecord.register("89873", "d4a48203516889f91940a55626807361")

    queried_record = record.replace(new_ip="192.168.3.1")
    assert queried_record.have_ip() is True
    assert queried_record.need_sync() is True
    assert queried_record.can_deploy() is True
