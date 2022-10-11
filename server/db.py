import os
import psycopg2

from typing import Dict, List, Tuple
from os.path import dirname
from dotenv import load_dotenv
from psycopg2 import Error

def get_from_dotenv(key):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)
    return os.getenv(key)

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(
        database=get_from_dotenv('POSTGRES_DB'),
        user=get_from_dotenv('POSTGRES_USER'),
        password=get_from_dotenv('POSTGRES_PASSWORD'),
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    def select(table_name: str, conditions: Dict):
        sql = f"SELECT * FROM {table_name}"
        if len(conditions) > 0:
            sql += " WHERE "
            for key in conditions.keys():
                sql += f"{key}={conditions[key]} AND "
            sql = sql[:-5]
        sql += ';'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def insert(table_name: str, column_values: Dict):
        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        cursor.execute(
            f"INSERT INTO {table_name} "
            f"({columns}) "
            f"VALUES {values[0]}",
            values)
        connection.commit()

    def get_version():
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        return record

    def update(table_name: str, fields: Dict, conditions: Dict):
        sql = f"UPDATE {table_name} SET "
        if len(fields) > 0:
            for key in fields.keys():
                sql += f"{key}={fields[key]},"
            sql = sql[:-1]
        else:
            return False
        if len(conditions) > 0:
            sql += " WHERE "
            for key in conditions.keys():
                sql += f"{key}={conditions[key]} AND "
            sql = sql[:-5]
        sql += ';'
        cursor.execute(sql)
        connection.commit()

    def delete(table_name: str, conditions: Dict):
        sql = f"DELETE FROM {table_name}"
        if len(conditions) > 0:
            sql += " WHERE "
            for key in conditions.keys():
                sql += f"{key}={conditions[key]} AND "
            sql = sql[:-5]
        sql += ';'
        print(sql)
        cursor.execute(sql)
        connection.commit()

    def need_message(user_id: int):
        sql = f"SELECT * FROM users WHERE user_id={user_id};"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
            return False
        else:
            return True

    def get_message_id(user_id: int):
        sql = f"SELECT * FROM users WHERE user_id={user_id};"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        if result is not None:
            return result[1]
        else:
            return None
            

except (Exception, Error) as error:
    print(error)

