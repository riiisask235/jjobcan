import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ID = os.environ.get("LOGIN_ID")
PWD = os.environ.get("PASSWORD")
TOKEN = os.environ.get("TOKEN")
