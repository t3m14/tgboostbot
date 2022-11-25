from peewee import *
from utils.models import *

def add_account(login, api_id, api_hash):
    try:
        acc = Account.create(login=login, api_id=api_id, api_hash=api_hash)
        db.close()
        return acc     
    except Exception as e:
        print(e)
        db.close()
        return
def delete_account(id):
    return Account.get_by_id(id).delete_instance()
def get_account_by_id(id):
    acc = Account.get_by_id(id)
    db.close()
    return {
        "id" : acc._pk,
        "login" : acc.login,
        "api_id" : acc.api_id,
        "api_hash" : acc.api_hash
    }
    
def get_all_accounts():
    accs = []
    for acc in Account.select():
        accs.append(
            {
                "id" : acc._pk,
                "login" : acc.login,
                "api_id" : acc.api_id,
                "api_hash" : acc.api_hash
            }
        )
    db.close()
    return accs
