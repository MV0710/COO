import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str('6416706304:AAHwOPIZ7-hB_9ahLiS99KwT5W9I-Q70ggk')
super_admins=[
    586619481,
    487868221,
    1097075145,
    1115993235

]
admins = [
    586619481,
    487868221,
    1097075145,
    1549715835,
    1115993235,
    537683865,
    764093692,
    1818324478
]
time_zone = 1

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

DATABASE = str(os.getenv("DATABASE"))
DB_USER = str(os.getenv("DB_USER"))
DB_PASS = str(os.getenv("DB_PASS"))
DB_HOST = str(os.getenv("DB_HOST"))
POSTGRES_URL = f'postgresql://{DB_USER}:{DB_PASS}@{ip}/{DATABASE}'
