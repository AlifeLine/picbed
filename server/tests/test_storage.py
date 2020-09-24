# -*- coding: utf-8 -*-

import json
import unittest
from config import REDIS
from utils.storage import MyRedis, is_json
from redis import Redis


class StorageTest(unittest.TestCase):

    def test_myredis(self):
        if REDIS:
            k = v = 'test'
            id1, id2 = ('index1', 'index2')
            jv = '"{}"'.format(v)
            nrc = MyRedis.from_url(REDIS, decode_responses=True)
            orc = Redis.from_url(REDIS, decode_responses=True)

            # test set/get
            nrc.delete(k)
            nrc.set(k, v)
            self.assertEqual(nrc.get(k), v)
            self.assertEqual(orc.get(k), jv)

            nrc.set(k, 123)
            self.assertIsInstance(nrc.get(k), int)
            self.assertEqual(nrc.get(k), 123)
            self.assertEqual(orc.get(k), "123")

            nrc.set(k, True)
            self.assertTrue(nrc.get(k))
            self.assertEqual(orc.get(k), 'true')

            jd = json.dumps(dict(a=1))
            nrc.set(k, jd)
            self.assertEqual(nrc.get(k), json.loads(jd))
            self.assertTrue(is_json(orc.get(k)))
            self.assertEqual(orc.get(k), jd)

            nrc.set(k, [])
            self.assertIsInstance(nrc.get(k), list)
            nrc.set(k, (1, ))
            self.assertIsInstance(nrc.get(k), list)

            # test hset/hget/hmget/hgetall
            nrc.delete(k)
            nrc.hset(k, k, v)
            self.assertEqual(nrc.hget(k, k), v)
            self.assertEqual(nrc.hmget(k, k), {k: v})
            self.assertEqual(orc.hget(k, k), jv)
            self.assertEqual(orc.hmget(k, k), [jv])
            nrc.hmset(k, dict(id1=id1, id2=id2))
            self.assertIsInstance(nrc.hmget(k, "id1", "id2"), dict)
            self.assertIsInstance(orc.hmget(k, "id1", "id2"), list)
            self.assertTrue("id1" in nrc.hmget(k, "id1"))
            self.assertTrue(nrc.hmget(k, "id1")["id1"], id1)
            self.assertTrue(orc.hmget(k, "id1")[0], '"{}"'.format(id1))
            self.assertIsInstance(nrc.hgetall(k), dict)

            # test_mypipeline
            nrc.delete(k)
            p = nrc.pipeline()
            p.set(k, v).execute()
            self.assertEqual(nrc.get(k), v)
            self.assertEqual(orc.get(k), jv)

            p.set(k, 666).execute()
            self.assertIsInstance(nrc.get(k), int)
            self.assertEqual(nrc.get(k), 666)

            orc.delete(k)
            p.hset(k, k, v).hmset(k, dict(id1=id1, id2=id2)).execute()
            ndata = nrc.hmget(k, k, 'id1', 'id2')
            self.assertIsInstance(ndata, dict)
            self.assertTrue(k in ndata)
            self.assertEqual(ndata[k], v)
            self.assertEqual(ndata["id1"], id1)
            odata = orc.hmget(k, k, 'id1', 'id2')
            self.assertIsInstance(odata, list)
            self.assertEqual(odata[0], jv)

            nrc.delete(k)


if __name__ == '__main__':
    unittest.main()
