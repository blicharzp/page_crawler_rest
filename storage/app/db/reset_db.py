import shelve

def reset_db(db_path, reset):
    if reset:
        with shelve.open(db_path) as db:
            db['content'] = []
