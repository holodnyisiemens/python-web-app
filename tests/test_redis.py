import pytest
from redis.asyncio import Redis


@pytest.mark.asyncio
async def test_redis_connection(redis: Redis):
    key = "test_key"
    pong = await redis.ping()
    assert pong is True

    await redis.set(key, "hello")
    value = await redis.get(key)
    assert value == "hello"

    await redis.delete(key)


@pytest.mark.asyncio
async def test_redis_with_str(redis: Redis):
    key = "user:name"
    await redis.set(key, "Иван")
    name = await redis.get(key)
    assert name == "Иван"
    await redis.delete(key)

    key = "session:123"
    # TTL в секундах
    await redis.setex(key, 10, "active")

    # проверяем, что значение установлено правильно
    value = await redis.get(key)
    assert value == "active"

    # проверяем, что TTL установлен
    ttl = await redis.ttl(key)
    assert ttl > 0
    assert ttl <= 10

    await redis.delete(key)


@pytest.mark.asyncio
async def test_redis_with_num(redis: Redis):
    key = "counter"
    await redis.set(key, 0)

    # incr увеличивает на 1
    await redis.incr(key)
    value = await redis.get(key)
    assert int(value) == 1

    await redis.incr(key)
    value = await redis.get(key)
    assert int(value) == 2

    # incrby на 5
    await redis.incrby(key, 5)
    value = await redis.get(key)
    assert int(value) == 7

    # decr уменьшает на 1
    await redis.decr(key)
    value = await redis.get(key)
    assert int(value) == 6

    # decrby на 3
    await redis.decrby(key, 3)
    value = await redis.get(key)
    assert int(value) == 3

    await redis.delete(key)


@pytest.mark.asyncio
async def test_redis_with_list(redis: Redis):
    key = "tasks"
    # добавление влево и вправо списка
    await redis.lpush(key, "task1", "task2")
    await redis.rpush(key, "task3", "task4")

    length = await redis.llen(key)
    assert length == 4

    tasks = await redis.lrange(key, 0, -1)
    assert tasks == ["task2", "task1", "task3", "task4"]

    first_task = await redis.lpop(key)
    assert first_task == "task2"

    last_task = await redis.rpop(key)
    assert last_task == "task4"

    await redis.delete(key)


@pytest.mark.asyncio
async def test_redis_with_set(redis: Redis):
    key_tags = "tags"
    key_langs = "languages"

    await redis.sadd(key_tags, "python", "redis", "database")
    await redis.sadd(key_langs, "python", "java", "js")

    tags_count = await redis.scard(key_tags)
    assert tags_count == 3

    is_member = await redis.sismember(key_tags, "python")
    assert is_member

    all_tags = await redis.smembers(key_tags)
    assert set(all_tags) == {"python", "redis", "database"}

    intersection = await redis.sinter(key_tags, key_langs)
    assert set(intersection) == {"python"}

    union = await redis.sunion(key_tags, key_langs)
    assert set(union) == {"python", "redis", "database", "java", "js"}

    difference = await redis.sdiff(key_tags, key_langs)
    assert set(difference) == {"redis", "database"}

    is_not_member = await redis.sismember(key_tags, "java")
    assert not is_not_member

    removed = await redis.srem(key_tags, "database")
    assert removed == 1

    tags_after_removal = await redis.smembers(key_tags)
    assert set(tags_after_removal) == {"python", "redis"}

    await redis.delete(key_tags)
    await redis.delete(key_langs)


@pytest.mark.asyncio
async def test_redis_with_hash(redis: Redis):
    key = "user:1000"
    hashmap = {"name": "Иван", "age": "30", "city": "Москва"}

    await redis.hset(key, mapping=hashmap)

    name = await redis.hget(key, "name")
    assert name == "Иван"

    all_data = await redis.hgetall(key)
    assert all_data == hashmap

    age_exists = await redis.hexists(key, "age")
    assert age_exists

    email_exists = await redis.hexists(key, "email")
    assert not email_exists

    keys = await redis.hkeys(key)
    assert set(keys) == {"name", "age", "city"}

    values = await redis.hvals(key)
    assert set(values) == {"Иван", "30", "Москва"}

    await redis.delete(key)


@pytest.mark.asyncio
async def test_redis_with_z(redis: Redis):
    key = "leaderboard"
    leaderboard = {"player1": 100, "player2": 200, "player3": 150}

    await redis.zadd(key, leaderboard)

    top_players = await redis.zrange(key, 0, 1)
    assert top_players == ["player1", "player3"]

    players_by_score = await redis.zrangebyscore(key, 100, 150)
    assert players_by_score == ["player1", "player3"]

    rank = await redis.zrank(key, "player1")
    assert rank == 0
