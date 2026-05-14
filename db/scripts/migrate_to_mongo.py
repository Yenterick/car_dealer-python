import sqlite3
import pymongo
import os
from datetime import datetime

# Project imports

from ui.consoleUtils import log

def migrate():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(base_dir, '..', 'car_dealer.db'))

    log(f"Connecting to SQLite: {db_path}...")
    
    try:
        # sqlite connection config
        sqlite_conn = sqlite3.connect(db_path)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()

        # mongo connection config
        mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        log(f"Connecting to MongoDB at {mongo_uri}...")
        mongo_client = pymongo.MongoClient(mongo_uri)
        mongo_client.server_info()
        
        mongo_db = mongo_client["car_dealer"]

        tables = ["supplier", "spare", "car", "customer", "employee", "buy", "sale"]

        for table in tables:
            log(f"Migrating table: {table}...")
            try:
                sqlite_cursor.execute(f"SELECT * FROM {table}")
                rows = sqlite_cursor.fetchall()
                
                collection = mongo_db[table]
                collection.delete_many({})
                
                if rows:
                    data = []
                    for row in rows:
                        item = dict(row)
                        pk_field = f"{table}_id"
                        if pk_field in item:
                            item['_id'] = item[pk_field]
                        
                        if 'created_at' in item and item['created_at']:
                            try:
                                ts = item['created_at']
                                if ' ' in ts:
                                    item['created_at'] = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                                elif 'T' in ts:
                                    item['created_at'] = datetime.fromisoformat(ts)
                            except (ValueError, TypeError):
                                pass
                        
                        data.append(item)
                    
                    collection.insert_many(data)
                    log(f"Successfully migrated {len(data)} documents to collection '{table}'...")
                else:
                    log(f"No data found in table '{table}'...")
            except Exception as e:
                log(f"Error migrating table {table}... {e}")

        sqlite_conn.close()
        mongo_client.close()
        log("Migration completed successfully...")

    except Exception as e:
        log(f"Error: Could not migrate the database... {e}")

if __name__ == "__main__":
    migrate()
