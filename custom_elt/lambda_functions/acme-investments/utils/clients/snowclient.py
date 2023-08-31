from snowflake.connector import connect, ProgrammingError
import os
from dotenv import load_dotenv

load_dotenv()


class SnowflakeConnection:
    def __init__(self):
        self.user = os.getenv("SNOWFLAKE_USER")
        self.account = os.getenv("SNOWFLAKE_ACCOUNT")
        self.warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
        self.database = os.getenv("SNOWFLAKE_DATABASE")
        self.schema = os.getenv("SNOWFLAKE_SCHEMA")
        self.password = os.getenv("SNOWFLAKE_PASSWORD")

    def connect(self):
        try:
            conn = connect(
                user=self.user,
                password=self.password,
                account=self.account,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
            )
            return conn
        except Exception as e:
            print("An error occurred while connecting to Snowflake:", str(e))
            raise

    def query(self, sql):
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
        except ProgrammingError as e:
            print("An error occurred while executing the query:", str(e))
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return results
