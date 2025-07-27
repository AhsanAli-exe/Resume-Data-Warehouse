import sqlite3
import pandas as pd

class DatabaseConnection:
    
    def __init__(self,db_path='../database/resume_warehouse.db'):
        self.db_path = db_path
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def execute_query(self,query,params=None):
        conn = self.get_connection()
        try:
            if params:
                df = pd.read_sql_query(query,conn,params=params)
            else:
                df = pd.read_sql_query(query,conn)
            return df
        finally:
            conn.close()
    
    def load_dataframe_to_table(self,df,table_name,if_exists='replace'):
        conn = self.get_connection()
        try:
            df.to_sql(table_name,conn,if_exists=if_exists,index=False)
            print(f"Loaded {len(df)} rows to {table_name}")
        finally:
            conn.close()
    
    def get_table_count(self, table_name):
        """Get row count for a table"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            return count
        finally:
            conn.close()

# Create a global instance
db = DatabaseConnection()
