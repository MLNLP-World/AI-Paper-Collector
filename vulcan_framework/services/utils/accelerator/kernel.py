import asyncio
import os
from typing import Optional, List, Union

import aiohttp
import gevent
from gevent.queue import Queue


class SteelTorrent:
    """轻量化的协程控件"""

    POWER = 4 if os.cpu_count() < 4 else 16

    def __init__(self, docker=None, debug: Optional[bool] = None):
        self.docker = docker
        self.debug = debug

        self.action_name = "SteelTorrent"

        self.pending_workers = Queue(self.POWER + 1)
        self.pending_jobs = Queue()
        self.done_jobs = Queue()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        while not self.pending_workers.empty():
            ctx_session = self.pending_workers.get()
            try:
                ctx_session.quit()
            except AttributeError:
                pass

    def _require_worker(self):
        """获取协同操作句柄"""

    def _release_worker(self, worker):
        """释放资源"""
        self.pending_workers.put(worker)

    def offload(self):
        """缓存卸载"""
        while not self.done_jobs.empty():
            yield self.done_jobs.get()

    def kernel(self):
        while not self.pending_jobs.empty():
            context = self.pending_jobs.get_nowait()
            self.perform(context)

    def perform(self, job):
        """插入的加速片段"""
        raise NotImplementedError

    def advance(self, jobs):
        for job in jobs:
            self.pending_jobs.put(job)

        # 弹出空载任务
        if self.pending_jobs.qsize() == 0:
            return

        # 启动分流核心
        kernel_matrix = []
        for _ in range(self.POWER):
            task = gevent.spawn(self.kernel)
            kernel_matrix.append(task)
        gevent.joinall(kernel_matrix)


class AshFramework:
    """轻量化的协程控件"""

    def __init__(self, docker: Optional[List] = None):
        # 任务容器：queue
        self.worker, self.done = asyncio.Queue(), asyncio.Queue()
        # 任务容器
        self.docker = docker
        # 任务队列满载时刻长度
        self.max_queue_size = 0

    def progress(self) -> str:
        """任务进度"""
        _progress = self.max_queue_size - self.worker.qsize()
        return f"{_progress}/{self.max_queue_size}"

    def preload(self):
        """预处理"""

    def overload(self):
        """任务重载"""
        if self.docker:
            for task in self.docker:
                self.worker.put_nowait(task)
        self.max_queue_size = self.worker.qsize()

    def offload(self) -> Optional[List]:
        """缓存卸载"""
        crash = []
        while not self.done.empty():
            crash.append(self.done.get())
        return crash

    async def control_driver(self, context, session=None):
        """需要并发执行的代码片段"""
        raise NotImplementedError

    async def launcher(self, session=None):
        """适配接口模式"""
        while not self.worker.empty():
            context = self.worker.get_nowait()
            await self.control_driver(context, session=session)

    async def subvert(self, workers: Union[str, int]):
        """
        框架接口

        loop = asyncio.get_event_loop()
        loop.run_until_complete(fl.go(workers))

        :param workers: ["fast", power]
        :return:
        """
        # 任务重载
        self.overload()

        # 弹出空载任务
        if self.max_queue_size == 0:
            return

        # 粘性功率
        workers = self.max_queue_size if workers in ["fast"] else workers
        workers = workers if workers <= self.max_queue_size else self.max_queue_size

        # 弹性分发
        task_list = []
        async with aiohttp.ClientSession() as session:
            for _ in range(workers):
                task = self.launcher(session=session)
                task_list.append(task)
            await asyncio.wait(task_list)
