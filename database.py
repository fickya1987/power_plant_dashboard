import sqlite3
import os.path
import pandas as pd

class Database:

    def __init__(self) -> None:

        # creating database object
        self.db = self._connecting()

        # creating cursor object
        self.cur = self.db.cursor()
    
    def _connecting(self):
        BASE_DIR = os.getcwd()
        db_path = os.path.join(BASE_DIR, r"db.db")

        try:
            db = sqlite3.connect(db_path, check_same_thread=False)
            print("connected!")
            return db
        except sqlite3.Error as e:
            print(e)

    def _germany_data(self): 
        
        sql_query = """
                SELECT 
                name, capacity_mw, primary_fuel, owner, source, latitude, longitude
                FROM
                global_power_plant_database
                WHERE
                country like "DEU"
                     """
        _df = pd.read_sql(sql_query, self.db)

        return _df.head(200) # returns a df