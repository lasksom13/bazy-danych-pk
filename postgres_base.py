import contextlib
import os
import subprocess
import time
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extensions import connection
from time import sleep
from abstract import BaseCommands
import typing as tp


class Postgres(BaseCommands):
    def __init__(
            self,
            host: str = "127.0.0.1",
            container_name: str = "postgres_db",
            image: str = "postgres:latest",
            password: str = "mysecretpassword",
            port: int = 9005
    ):
        self._host = host
        self._container_name = container_name
        self._image = image
        self._password = password
        self._port = port

    def start_database(
            self
    ) -> None:
        """
        run docker image of postgres database
        """
        try:
            subprocess.run(['docker', 'run', '-d', '--name', self._container_name, '-p', f'{self._port}:5432', '-e',
                            f'POSTGRES_PASSWORD={self._password}', self._image])
        except Exception as e:
            print("Error when start_database")
            print("error type: ", type(e))
            print(str(e))

    def connect(self) -> connection:
        """
        :return: object that allows user to communicate with postgres database
        """
        conn = psycopg2.connect(
            host=self._host,
            port=self._port,
            database='postgres',
            user='postgres',
            password=self._password
        )
        return conn

    def create_table(
            self,
            table_name: str = "imdbdata"
    ) -> None:
        """
        :return: create table according to  our tsv file
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"""
                CREATE TABLE {table_name} (
                    tconst TEXT PRIMARY KEY,
                    titleType TEXT,
                    primaryTitle TEXT,
                    originalTitle TEXT,
                    isAdult BOOLEAN,
                    startYear TEXT,
                    endYear TEXT,
                    runtimeMinutes TEXT,
                    genres TEXT[]
                )
            """)
        conn.commit()
        cursor.close()
        conn.close()

    def test_time_for_insert(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata"
    ) -> float:
        """
        :return: amount of time it takes to insert records to table
        """
        start_time = time.time()
        conn = self.connect()
        cursor = conn.cursor()
        with open("." + os.path.sep + "title.basics.tsv" + os.path.sep + "data.tsv", 'r', encoding='utf-8') as file:
            next(file)  # Skip header line
            iterator = 0
            data = []
            for line in file:
                if iterator >= record_amount:
                    break
                fields = line.strip().split('\t')
                fields[4] = fields[4] == '1'  # Convert isAdult field to boolean
                fields[8] = fields[8].split(',') if len(fields) > 8 else []  # Convert genres to list
                data.append(fields)
                iterator += 1
            execute_values(cursor, f"""
                    INSERT INTO {table_name} (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
                    VALUES %s
                """, data)
        conn.commit()
        cursor.close()
        conn.close()
        end_time = time.time()
        return end_time - start_time

    def get_record_amount(
            self,
            table_name: str = "imdbdata"
    ) -> int:
        """
        :return: amount of records inside table
        """
        conn: connection = self.connect()
        cursor = conn.cursor()
        cursor.execute(fr"SELECT COUNT(*) FROM {table_name} ")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    def list_tables(
            self
    ) -> tp.List:
        """
        :return: list with table names
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        table_names = cursor.fetchall()
        tables = [table_name[0] for table_name in table_names]
        # for table_name in table_names:
        #     print(table_name[0])
        cursor.close()
        conn.close()
        return tables

    def drop_table(
            self,
            table_name: str = "imdbdata"
    ) -> None:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
        cursor.close()
        conn.close()

    def get_primary_key_column(
            self,
            table_name: str = "imdbdata"
    ):
        """
        :return: name of primary key column
        """
        conn = self.connect()
        cursor = conn.cursor()
        query = """
            SELECT a.attname
            FROM pg_catalog.pg_constraint AS c
            JOIN pg_catalog.pg_class AS t ON c.conrelid = t.oid
            JOIN pg_catalog.pg_attribute AS a ON a.attnum = ANY(c.conkey) AND a.attrelid = t.oid
            WHERE c.contype = 'p' AND t.relname = %s
            """
        cursor.execute(query, (table_name,))
        primary_key_column = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return primary_key_column

    def get_column_names(
            self,
            table_name: str = "imdbdata"
    ):
        """
        :return: list of column names
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        columns = cursor.fetchall()
        column_list = [column[0] for column in columns]
        cursor.close()
        conn.close()
        return column_list

    def test_time_for_delete(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata"
    ) -> float:
        start_time = time.time()
        conn = self.connect()
        cursor_select = conn.cursor()
        cursor_del = conn.cursor()
        cursor_select.execute(f"SELECT * FROM {table_name}")
        primary_key_column = self.get_primary_key_column(table_name=table_name)
        iterator = 0
        while True:
            record = cursor_select.fetchone()
            # print(record)
            if record is None or iterator >= record_amount:
                break
            iterator += 1
            # if primary key is in first table column
            primary_key = record[0]
            # tconst is name of our primary key column
            cursor_del.execute(f"DELETE FROM {table_name} WHERE {primary_key_column} = '{primary_key}'")
            # # commit after each record delete
            # conn.commit()
        conn.commit()
        cursor_select.close()
        cursor_del.close()
        conn.close()
        end_time = time.time()
        return end_time - start_time

    def test_time_for_modify(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata",
            values: tp.Optional[tp.List] = [
                    'short',
                    'Boulevard des Italiens',
                    'Boulevard des Italiens',
                    False,
                    '1896',
                    r'\N',
                    r'\N',
                    ['Documentary', 'Short']]
    ) -> float:
        """
        to pewnie trzeba poprawić ale coś mi nie działało puszczanie query i po takiej zmianie dopiero poszło)
        """
        start_time = time.time()
        conn = self.connect()
        cursor_select = conn.cursor()
        cursor_update = conn.cursor()
        primary_key_column = self.get_primary_key_column(table_name=table_name)
        cursor_select.execute(f"SELECT * FROM {table_name} LIMIT {record_amount}")
        update_query = (
            "UPDATE " + table_name + " SET "
            "titleType = %s, "
            "primaryTitle = %s, "
            "originalTitle = %s, "
            "isAdult = %s, "
            "startYear = %s, "
            "endYear = %s, "
            "runtimeMinutes = %s, "
            "genres = %s "
            "WHERE " + primary_key_column + " = %s"
        )
        for row in cursor_select.fetchall():
            # assume primary key is first
            primary_key_value = row[0]
            values_with_primary_key = values + [primary_key_value]
            print(values_with_primary_key)
            print(len)
            cursor_update.execute(update_query, values_with_primary_key)
        conn.commit()
        cursor_select.close()
        cursor_update.close()
        conn.close()
        end_time = time.time()
        return end_time - start_time

    def test_time_for_record_amount_with_word(
            self,
            field_name: str,
            search_word: str,
            table_name: str = "imdbdata"
    ) -> float:
        pass

    def test_time_for_user_query(
            self,
            query: str = "SELECT * FROM imdbdata LIMIT 50"
    ) -> tp.Tuple[float, tp.List]:
        """
        :return: tuple (time to execute, result_of_query as list)
        """
        start_time = time.time()
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        end_time = time.time()
        for row in rows:
            print(row)
        return end_time - start_time, rows

    def test_time_for_max(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        start_time = time.time()
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX({column_name}) FROM {table_name} "
                       f"WHERE {column_name} IS NOT NULL "
                       fr"AND {column_name} != E'\\N'")
        max_value = cursor.fetchone()[0]
        print(max_value)
        cursor.close()
        conn.close()
        end_time = time.time()
        return end_time-start_time, max_value

    def test_time_for_min(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        start_time = time.time()
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT MIN({column_name}) FROM {table_name} "
                       f"WHERE {column_name} IS NOT NULL "
                       fr"AND {column_name} != E'\\N'")
        min_value = cursor.fetchone()[0]
        print(min_value)
        cursor.close()
        conn.close()
        end_time = time.time()
        return end_time-start_time, min_value

    def test_time_for_sorting(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        start_time = time.time()
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY {column_name}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        end_time = time.time()
        for row in rows:
            print(row)
        return end_time - start_time, rows

    def test_time_for_median(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        """
        value in the middle of sorted records based on column_name (use with "runtimeMinutes")
        :return:
        """
        start_time = time.time()
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {column_name}::numeric) FROM {table_name} "
                       f"WHERE {column_name} IS NOT NULL "
                       fr"AND {column_name} != E'\\N'")
        median = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        end_time = time.time()
        return end_time - start_time, median

    def test_time_for_data_distribution(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        """
        group_by + count (use with "runtimeMinutes")
        :return:
        """
        start_time = time.time()
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column_name}, COUNT(*) FROM {table_name} GROUP BY {column_name} "
                       f"HAVING {column_name} IS NOT NULL "
                       fr"AND {column_name} != E'\\N'")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        end_time = time.time()
        return end_time - start_time, rows


if __name__ == "__main__":
    # main()
    print("start")
    ins = Postgres()
