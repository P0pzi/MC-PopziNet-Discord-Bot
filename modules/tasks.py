import json
import threading

import time
import schedule
import yaml
import os.path
from datetime import datetime

from yaml import Loader


class Task:
    def __init__(self, name: str, task: str, dt: datetime, args_json: str = ""):
        self.name = name
        self.task = task
        self.dt = dt
        self.args_json = args_json

    def as_dict(self):
        return {
            'name': self.name,
            'task': self.task,
            'dt': self.dt,
            'args_json': self.args_json
        }

    @staticmethod
    def from_dict(_dict):
        return Task(
            name=_dict['name'],
            task=_dict['task'],
            dt=_dict['dt'],
            args_json=_dict['args_json'],
        )


class TaskModule:
    TASK_THREAD = None

    tasks = {}
    runnables = {}

    task_filename = None

    def __init__(self, task_filename):
        self.load_tasks(task_filename)

    @property
    def file_exists(self) -> bool:
        return os.path.exists(self.task_filename)

    def add_runnable(self, name: str, runnable):
        self.runnables[name] = runnable

    def load_tasks(self, task_filename):
        self.task_filename = task_filename
        self.tasks = {}
        if self.file_exists:
            file = open(task_filename, 'r')
            contents = yaml.load(file, Loader=Loader)

            if contents and 'tasks' in contents:
                self.tasks = {t.name: t for t in [Task.from_dict(t) for t in contents['tasks']]}

    def save_tasks(self) -> bool:
        if not self.task_filename:
            return False

        file = open(self.task_filename, 'w')
        yaml.dump({'tasks': [t.as_dict() for t in list(self.tasks.values())]}, file)
        return True

    def add_task(self, task) -> None:
        if task.task not in self.runnables:
            print(f'{task.task} not defined as runnable')
            return

        self.tasks[task.name] = task
        self.save_tasks()

    def remove_task(self, task_name: str, save=True) -> None:
        self.tasks[task_name] = None
        del self.tasks[task_name]
        save and self.save_tasks()

    def handle_run(self):
        now = datetime.now()
        for task in list(self.tasks.values()):
            if task.dt < now:
                runnable_str = task.task
                runnable = self.runnables[runnable_str]

                if runnable:
                    task_args = json.loads(task.args_json)
                    runnable(*task_args)
                    self.remove_task(task.name, save=False)

        self.save_tasks()

    # Make sure this runs in a separate thread, as it's blocking
    def runner(self):
        schedule.every(1).minute.do(self.handle_run)
        while True:
            schedule.run_pending()
            time.sleep(30)

    def start(self):
        if not self.TASK_THREAD:
            self.TASK_THREAD = threading.Thread(target=self.runner)
            self.TASK_THREAD.start()
