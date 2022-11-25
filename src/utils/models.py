from peewee import *

db = SqliteDatabase('accs_database.db', timeout=10)


class Account(Model):
    login = CharField(unique=True)
    api_id = CharField()
    api_hash = CharField()
    class Meta:
        database = db

# if __name__ == '__main__':
#     try:
#         db.connect()
#         Account.create_table()
#         db.close()
#     except InternalError as px:
#         print(str(px))