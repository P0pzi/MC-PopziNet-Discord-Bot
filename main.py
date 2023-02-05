import os

from dotenv import load_dotenv

from poopz import PoopzClient

print("Poopz Initializing...")

# Ensure Environmental variables are set
load_dotenv()
expected_envs = ['DISCORD_BOT_SECRET', 'MC_SERVER_IP', 'MC_SERVER_PORT']

for env in expected_envs:
    assert os.getenv(env)
    print("Loaded OS Env:", env + '=' + os.getenv(env))


def runnable_method(one_arg):
    print(f'Hello, {one_arg}')


poopz = PoopzClient()
poopz.run(os.getenv('DISCORD_BOT_SECRET'))
