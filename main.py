import json
import os
import datetime
from datetime import timedelta

from dotenv import load_dotenv

from modules.tasks import TaskModule, Task
from poopz import PoopzClient

# Ensure Environmental variables are set
load_dotenv()
assert os.getenv('CLIENT_SECRET')
assert os.getenv('MC_SERVER_IP')
assert os.getenv('MC_SERVER_PORT')


def runnable_method(one_arg):
    print(f'Hello, {one_arg}')


task_module = TaskModule("tasks.yaml")
task_module.add_runnable('run', runnable_method)

# Runs in one minute from now
task_module.add_task(Task(
    'test 1',
    'run',
    datetime.datetime.now() + timedelta(minutes=1),
    json.dumps(['World 2'])
))

# Runs right away, as it should already have been run
task_module.add_task(Task(
    'test 2',
    'run',
    datetime.datetime.now() - timedelta(minutes=1),
    json.dumps(['World 1'])
))

task_module.start()

PoopzClient().run(os.getenv('CLIENT_SECRET'))
