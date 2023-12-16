import motor.motor_asyncio

# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')


username = 'coolgameadmin'
password = 'iyu1vap8'
host = 'localhost'  # или IP-адрес сервера MongoDB
port = '27017'  # стандартный порт MongoDB
database = 'coolgame_admin'

# Формирование строки подключения
connection_string = f"mongodb://{username}:{password}@{host}:{port}/{database}"

client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{username}:{password}@{host}:{port}/{database}')

db = client.coolgame_admin

collection = db.games
