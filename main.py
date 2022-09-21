import os

from dotenv import load_dotenv
from poopz import PoopzClient

# Ensure Environmental variables are set
load_dotenv()
assert os.getenv('CLIENT_SECRET')
assert os.getenv('MC_SERVER_IP')
assert os.getenv('MC_SERVER_PORT')

PoopzClient().run(os.getenv('CLIENT_SECRET'))
