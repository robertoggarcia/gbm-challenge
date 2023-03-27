from app.db.in_memory import InMemoryManager


class FakeInMemoryManager(InMemoryManager):
    salt = "test_salt"
    lifetime = 60


def test_in_memory_manager_set(in_memory_instance):
    fake_in_memory = FakeInMemoryManager()
    assert not fake_in_memory._redis.get("fake_key")

    fake_in_memory.set(key="fake_key", value=1)

    assert fake_in_memory.get("fake_key") == 1


def test_in_memory_manager_get(in_memory_instance):
    fake_in_memory = FakeInMemoryManager()
    fake_in_memory._redis.set("fake_key", 1, ex=60)

    assert fake_in_memory.get("fake_key") == 1
