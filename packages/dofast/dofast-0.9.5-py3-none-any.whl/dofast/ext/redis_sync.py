import json
import sys
from base64 import b64decode, b64encode
from typing import List

import codefast as cf
import redis
import joblib
from uuidentifier import snowflake

from dofast.pipe import author
from dofast.vendor.command import Command


class RedisSync(Command):
    def __init__(self):
        super().__init__()
        self.session_file = cf.io.dirname() + '/redis_sync_session.joblib'
        self.name = 'redis_sync'
        self.description = 'Sync data between Redis and local file system.'
        self.subcommands = [['st', 'sync_to_redis'], ['sf', 'sync_from_redis']]
        self.cli = None

    def load_session(self):
        """Load session from file."""
        acc: dict
        try:
            acc = joblib.load(self.session_file)
        except Exception as e:
            cf.warning('Failed to load session file: {}'.format(e))
            acc = json.loads(author.get('DATA_REDIS').replace('\'', '"'))
            joblib.dump(acc, self.session_file)

        self.cli = redis.StrictRedis(host=acc['host'],
                                     port=acc['port'],
                                     password=acc['password'])

    def sync_from_redis(self) -> True:
        self.load_session()
        cf.info(json.loads(self.cli.get('redis_sync_task_info')))
        js = json.loads(self.cli.get(self.name))
        for k, v in js.items():
            cf.info('sync from server: {}'.format(k))
            with open(k, 'wb') as f:
                f.write(b64decode(v))
        return True

    def sync_to_redis(self, files: List[str]) -> bool:
        """Encode file to binary and store in Redis."""
        self.load_session()

        def _encode_file(f: str):
            return b64encode(open(f, 'rb').read()).decode('utf-8')

        js = {cf.io.basename(f): _encode_file(f) for f in files}
        js = json.dumps(js)
        task_info = json.dumps({'files': files, 'uuid': snowflake.uuid()})
        cf.info('sync to server: {}'.format(files))
        self.cli.set(self.name, js)
        self.cli.set('redis_sync_task_info', task_info)
        cf.info('sync complete')
        return True

    def _process(self, args: None) -> bool:
        if not args:
            self.sync_from_redis()
        else:
            self.sync_to_redis(args)


def entry():
    RedisSync()._process(sys.argv[1:])
