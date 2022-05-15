import mysql.connector
import logging
import pandas
from datetime import date

logging.basicConfig(filename=f'Log-{date.today().strftime("%b-%d-%Y")}.log', level=logging.INFO)


class DB_CONNECTION:

    def __init__(self):
        self.database_connection = None

    @staticmethod
    def establish_connection(user, password):
        try:
            conn = mysql.connector.connect(host="localhost", user=user, password=password)  # "Vvu8z9D"
            return conn, True
        except mysql.connector.Error as error:
            logging.debug(f"MySQL Error during Connection {error}")
            return None, False
        except Exception as error:
            logging.debug(f"Unknown Error {error}")
            return None, False


class CRUD(DB_CONNECTION):
    def __init__(self):
        DB_CONNECTION.__init__(self)

    @staticmethod
    def create_table(database_connection, database_name, table_name, create_command):
        try:
            database_cursor = database_connection.cursor()
            database_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            database_cursor.execute(f"DROP TABLE IF EXISTS {database_name}.{table_name}")
            database_cursor.execute(create_command)
            database_connection.commit()
            database_cursor.close()
            return True
        except mysql.connector.Error as error:
            logging.debug(f"MySQL Error during CREATE {error}")
            return False
        except Exception as error:
            logging.debug(f"Unknown Error {error}")
            return False
        finally:
            if database_cursor in locals():
                database_cursor.close()

    @staticmethod
    def insert_values(database_connection, insert_command, insert_values):
        try:
            database_cursor = database_connection.cursor()
            database_cursor.executemany(insert_command, insert_values)
            database_connection.commit()
            database_cursor.close()
            return True
        except mysql.connector.Error as error:
            logging.debug(f"MySQL Error during INSERT {error}")
            return False
        except Exception as error:
            logging.debug(f"Unknown Error {error}")
            return False
        finally:
            if database_cursor in locals():
                database_cursor.close()

    @staticmethod
    def update_values(database_connection, update_command):
        try:
            database_cursor = database_connection.cursor()
            database_cursor.execute(update_command)
            database_connection.commit()
            database_cursor.close()
            return True
        except mysql.connector.Error as error:
            logging.debug(f"MySQL Error during UPDATE {error}")
            return False
        except Exception as error:
            logging.debug(f"Unknown Error {error}")
            return False
        finally:
            if database_cursor in locals():
                database_cursor.close()

    @staticmethod
    def delete_rows(database_connection, database_name, table_name, primary_key, key_value):
        try:
            database_cursor = database_connection.cursor()
            delete_command = f'DELETE FROM {database_name}.{table_name} WHERE {primary_key}={key_value}'
            database_cursor.execute(delete_command)
            database_connection.commit()
            database_cursor.close()
            return True
        except mysql.connector.Error as error:
            logging.debug(f"MySQL Error during DELETE {error}")
            return False
        except Exception as error:
            logging.debug(f"Unknown Error {error}")
            return False
        finally:
            if database_cursor in locals():
                database_cursor.close()

    @staticmethod
    def backup(database_connection, database_name, table_name):
        try:
            database_cursor = database_connection.cursor()
            '''database_cursor.execute(f"DROP TABLE IF EXISTS {database_name}.{table_name}_backup")
            backup_command = f'CREATE TABLE {database_name}.{table_name}_backup ' \
                             f'SELECT * FROM {database_name}.{table_name}' '''
            command = f'SELECT * FROM {database_name}.{table_name}'
            database_cursor.execute(command)
            result = database_cursor.fetchall()
            result_df = pandas.read_sql(command, database_connection)
            result_df.to_csv('File.csv', index=False)
            database_connection.commit()
            database_cursor.close()
            return True
        except mysql.connector.Error as error:
            logging.debug(f"MySQL Error during BACKUP {error}")
            return False
        except Exception as error:
            logging.debug(f"Unknown Error {error}")
            return False
        finally:
            if database_cursor in locals():
                database_cursor.close()
