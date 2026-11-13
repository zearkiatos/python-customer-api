import os
from dotenv import load_dotenv

environment = os.getenv("ENVIRONMENT")

if environment == 'local':
    load_dotenv(dotenv_path='.env.local')
elif environment == "test":
    load_dotenv(dotenv_path='.env.test')
else:
    load_dotenv(dotenv_path='.env')


class Config:
    ENVIRONMENT = environment
    DATABASE_URL=os.getenv('DATABASE_URL')
    DEPENDENCY_DATABASE_TYPE=os.getenv('DEPENDENCY_DATABASE_TYPE')