import os

from dotenv import load_dotenv
from poopz import PoopzClient

# Ensure Environmental variables are set
load_dotenv()
assert os.getenv('CLIENT_SECRET')
assert os.getenv('MC_SERVER_IP')
assert os.getenv('MC_SERVER_PORT')

PoopzClient().run(os.getenv('CLIENT_SECRET'))

#
# def runnable_method(one_arg):
#     print(f'Hello, {one_arg}')
#
#
# task_module = TaskModule("tasks.yaml")
# task_module.add_runnable('run', runnable_method)
#
# task_module.add_task(Task(
#     'test',
#     'run',
#     datetime.datetime.now(),
#     json.dumps(['World'])
# ))
#
# task_module.start()

