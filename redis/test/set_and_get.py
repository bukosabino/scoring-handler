import unittest

import fakeredis


class RedisTest(unittest.TestCase):
    def test_set_and_get(self):
        expected_value = "bar"
        redis_connector = fakeredis.FakeStrictRedis(host="localhost", port=6379, db=0)
        set_response = redis_connector.set("foo", expected_value)
        self.assertTrue(set_response)
        get_response = redis_connector.get("foo")
        self.assertEqual(get_response.decode("ascii"), expected_value)
