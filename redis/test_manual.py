"""Util test, to check if Redis is ready to work.
"""

import redis

expected_value = "bar"
redis_connector = redis.Redis(host="localhost", port=6379, db=0)
set_response = redis_connector.set("foo", expected_value)
get_response = redis_connector.get("foo")
print(get_response)
