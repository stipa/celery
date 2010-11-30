from gevent.greenlet import Greenlet
from gevent.pool import Pool

from celery.concurrency.base import apply_target, BasePool


class TaskPool(BasePool):

    def on_start(self):
        self._pool = Pool(self.limit)

    def on_stop(self):
        if self._pool is not None:
            self._pool.join()

    def on_apply(self, target, args=None, kwargs=None, callback=None,
            accept_callback=None, **_):
        return self._pool.spawn(apply_target, target, args, kwargs,
                                callback, accept_callback)

    @classmethod
    def on_import(cls):
        from gevent import monkey
        monkey.patch_all()
TaskPool.on_import()