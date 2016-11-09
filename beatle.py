import aiohttp
import argparse
import asyncio
import hmac
import logging
import os
import raftos

from configparser import ConfigParser, NoSectionError, NoOptionError
from datetime import datetime, timedelta
from logging.handlers import SysLogHandler

from crontab import CronTab


logger = logging.getLogger('beatle')


DEFAULT_CONFIGURATION = {
    'LOOP_TIMEOUT': 10,
    'UPDATE_EVERY': 600,
    'TIMEOUT': 5,
    'TIME_ZONE': 'Europe/Moscow'
}


class Beatle:
    def __init__(self, config_path, beatle_id):
        self.id = beatle_id
        self.read_config(config_path)
        self.init_logger()

    def config_get(self, section, option, default=None):
        try:
            return self.config.get(section, option)
        except (NoSectionError, NoOptionError):
            return default

    def read_config(self, config_path):
        self.config = ConfigParser()
        self.config.read(config_path)

        self.loop_timeout = int(self.config_get('beatle', 'LOOP_TIMEOUT', 10))

        self.projects = []
        for section in self.config.sections():
            if section != 'beatle':
                configuration = DEFAULT_CONFIGURATION.copy()
                configuration.update({
                    'NAME': section,
                    'KEY': self.config_get(section, 'KEY'),
                    'URL': self.config_get(section, 'URL'),

                    'UPDATE_EVERY': self.config_get('beatle', 'UPDATE_EVERY', 600),
                    'TIMEOUT': self.config_get('beatle', 'TIMEOUT', 5),
                    'TIME_ZONE': self.config_get('beatle', 'TIME_ZONE', 'Europe/Moscow'),

                    'LOOP_TIMEOUT': self.loop_timeout,
                })
                self.projects.append(Project(self, configuration))

    def init_logger(self):
        logger.setLevel(logging.DEBUG)
        facility = self.config_get('logging', 'facility', 'LOG_USER')

        handler = SysLogHandler(facility=getattr(SysLogHandler, facility))
        logger.addHandler(handler)

    async def run(self):
        """Run event loop"""
        loop = asyncio.get_event_loop()
        while True:
            if raftos.get_leader() == self.id:
                for project in self.projects:
                    loop.create_task(project.call())

            await asyncio.sleep(self.loop_timeout)


class Project:
    def __init__(self, beatle, configuration):
        self.beatle = beatle

        self.name = configuration.get('NAME')
        self.key = configuration.get('KEY')
        self.url = configuration.get('URL')

        self.timezone = configuration.get('TIME_ZOME')
        self.update_every = int(configuration.get('UPDATE_EVERY'))
        self.timeout = int(configuration.get('TIMEOUT'))

        self.loop_timeout = int(configuration.get('LOOP_TIMEOUT'))

        self.last_update = None

        self.config = {}
        self.tasks = {}

    async def get_config(self):
        """Return config from projects' HTTP endpoint"""

        if self.config_have_to_be_updated:
            self.config = await self._request('get') or self.config or {}

            self.tasks = {
                CronTab(cron_string): task
                for task, cron_string in self.config.get('TASKS', {}).items()
            }

            self.timezone = self.config.get('TIME_ZONE') or self.timezone
            self.timeout = self.config.get('TIMEOUT') or self.timeout
            self.update_every = self.config.get('UPDATE_EVERY') or self.update_every

            self.last_update = datetime.now()

    def config_have_to_be_updated(self):
        if self.last_update is None:
            return True

        return self.last_update < datetime.now() - timedelta(self.update_every)

    async def call(self):
        """POST to HTTP endpoint if needed"""

        await self.get_config()

        task_list = [
            task_name for cron, task_name in self.tasks.items()
            if cron.next() < self.loop_timeout
        ]
        if task_list:
            return await self._request('post', params={'TASKS': task_list})

    async def _request(self, method, params=None):
        if params is None:
            params = {}
        params.update({'SIGNATURE': self._get_signature(params)})

        request = getattr(aiohttp, method)
        with aiohttp.Timeout(self.timeout):
            async with request(self.url, params=params) as r:
                if r.status != 200:
                    return
                return await r.json()

    def _get_signature(self, params):
        msg = ''.join(map(str, sorted(params.values()))).encode()
        return hmac.new(self.key.encode(), msg=msg).hexdigest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf')
    parser.add_argument('--node')
    parser.add_argument('--cluster')
    args = parser.parse_args()

    cluster = ['127.0.0.1:{}'.format(port) for port in args.cluster.split()]
    node = '127.0.0.1:{}'.format(args.node)

    raftos.register(node, cluster=cluster)
    beatle = Beatle(config_path=args.conf, beatle_id=node)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(beatle.run())
    loop.close()
