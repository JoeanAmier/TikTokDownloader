# -*- coding: utf-8 -*-
# @Author : Frica01
# @Time   : 2023-12-28 23:24
# @Name   : model_main.py

from collections import defaultdict

from PySide6.QtCore import (QRunnable, QObject, QThreadPool, Signal, Slot)


class WorkerRunnable(QRunnable):

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.kwargs = kwargs
        self.args = args
        self.signal = kwargs.get('signal')
        self.thread_name = kwargs.get('thread_name')
        self.signal_thread = kwargs.get('signal_thread')

    def run(self):
        for func in self.func:
            func(*self.args)
        self.signal.emit(True)
        self.signal_thread.emit(self.thread_name)

    def run_other(self):
        self.func(*self.args)
        self.signal_thread.emit(self.thread_name)

    def run_live(self):
        live_data = [self.func(*self.args, **param).run() for param in self.kwargs['params']]
        self.signal.emit(live_data)
        self.signal_thread.emit(self.thread_name)


class ModelMain(QObject):
    signal_initial = Signal(bool)
    signal_live = Signal(list)
    signal_change_status = Signal(str)

    def __init__(self):
        super().__init__()
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(10)
        self.task_status_map = defaultdict(bool)
        self.signal_change_status.connect(self.change_task_status)

    def initial(self, func_list, *args, **kwargs):
        thread_name = 'init'
        if self.task_status_map.get(thread_name):
            return
        self.task_status_map[thread_name] = True
        task = WorkerRunnable(
            func_list,
            thread_name=thread_name,
            signal=self.signal_initial,
            signal_thread=self.signal_change_status,
            *args,
            **kwargs
        )
        self.thread_pool.start(task)

    def run_task(self, func, *args, **kwargs):
        thread_name = kwargs.get('thread_name')
        if self.task_status_map.get(thread_name):
            return
        self.task_status_map[thread_name] = True
        # print('====> 我启动了', self.task_status_map)
        task = WorkerRunnable(
            func,
            *args,
            # **kwargs,
            thread_name=thread_name,
            signal_thread=self.signal_change_status
        )
        self.thread_pool.start(task.run_other)

    def run_live(self, func, *args, **kwargs):
        thread_name = 'mode_4'
        if self.task_status_map.get(thread_name):
            return
        self.task_status_map[thread_name] = True
        task = WorkerRunnable(
            func,
            *args,
            **kwargs,
            signal=self.signal_live,
            thread_name=thread_name,
            signal_thread=self.signal_change_status
        )
        self.thread_pool.start(task.run_live)

    @Slot(str)
    def change_task_status(self, thread_name: str):
        del self.task_status_map[thread_name]