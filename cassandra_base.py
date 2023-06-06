import subprocess
import time

from cassandra.cluster import Cluster
import typing as tp
from time import sleep
from abstract import BaseCommands
import typing as tp
import os
from cassandra.query import BatchStatement, SimpleStatement, ConsistencyLevel


class CassandraDB():
    def __init__(
            self,
            host: str = "127.0.0.1",
            container_name: str = "cassandra_db",
            port: int = 9008
    ):
        self._host = host
        self._container_name = container_name
        self._port = port

    def start_database(self) -> None:
        """
        Run Cassandra container
        """
        try:
            subprocess.run(['docker', 'run', '-d', '--name', self._container_name, '-p', f'{self._port}:9042', 'cassandra'])
            sleep(10)  # Wait for Cassandra to start
        except Exception as e:
            print("Error when starting the database")
            print("Error type: ", type(e))
            print(str(e))

    def connect(self):
        cluster = Cluster([self._host],
                          port=self._port)
        session = cluster.connect()

        replication_strategy = {
            'class': 'SimpleStrategy',
            'replication_factor': 1  # Adjust the replication factor as per your requirements
        }
        keyspace = "mydatabase"
        query = f"CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH REPLICATION = {replication_strategy};"
        session.execute(query)
        session.set_keyspace(keyspace)
        return session

    def create_table(self, table_name: str = "imdbdata") -> None:
        session = self.connect()
        # query = f"CREATE TABLE mydatabase.{table_name} (tconst text PRIMARY KEY, titleType text, primaryTitle text, " \
        #         f"originalTitle text, isAdult boolean, startYear text, endYear text, runtimeMinutes text, genres list<text>)"
        # session.execute(query)
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                tconst TEXT PRIMARY KEY,
                titleType TEXT,
                primaryTitle TEXT,
                originalTitle TEXT,
                isAdult BOOLEAN,
                startYear TEXT,
                endYear TEXT,
                runtimeMinutes TEXT,
                genres LIST<TEXT>
            )
        """
        session.execute(create_table_query)

    def drop_table(self, table_name: str = "imdbdata") -> None:
        session = self.connect()
        query = f"DROP TABLE IF EXISTS mydatabase.{table_name}"
        session.execute(query)

    def test_time_for_insert(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata",
            values: tp.Optional[tp.List] = None
    ) -> float:
        start_time = time.time()
        session = self.connect()

        with open("." + os.path.sep + "title.basics.tsv" + os.path.sep + "data_cassandra.tsv", 'r', encoding='utf-8') as file:
            next(file)  # Skip header line
            iterator = 0
            batch_size = 100  # Adjust batch size as needed
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
            record_amount += 1
            for line in file:
                if iterator >= record_amount:
                    break
                fields = line.strip().split('\t')
                fields[4] = bool(int(fields[4]))  # Convert isAdult field to boolean
                fields[8] = fields[8].split(',') if len(fields) > 8 else []  # Convert genres to list

                # query = f"INSERT INTO mydatabase.{table_name} (tconst, titleType, primaryTitle, originalTitle, isAdult, " \
                #         f"startYear, endYear, runtimeMinutes, genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                # session.execute(query, (
                #     fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8]
                # ))

                #fields = [field.replace("'", "") if isinstance(field, str) else field for field in fields]

                query = f"INSERT INTO mydatabase.{table_name} (tconst, titleType, primaryTitle, originalTitle, isAdult, " \
                        f"startYear, endYear, runtimeMinutes, genres) VALUES ('{fields[0]}', '{fields[1]}', '{fields[2]}', " \
                        f"'{fields[3]}', {fields[4]}, '{fields[5]}', '{fields[6]}', '{fields[7]}', {fields[8]})"
                # print(query)
                # session.execute(query)
                batch.add(SimpleStatement(query))
                if iterator % batch_size == 0:
                    session.execute(batch)
                    batch.clear()

                iterator += 1

        end_time = time.time()
        return end_time - start_time

    # def test_time_for_delete(
    #         self,
    #         record_amount: int = 10000,
    #         table_name: str = "imdbdata"
    # ) -> float:
    #     """
    #      wyrzucam po jednym
    #     """
    #     start_time = time.time()
    #     session = self.connect()
    #
    #     query = f"SELECT tconst FROM mydatabase.{table_name} LIMIT {record_amount}"
    #     result = session.execute(query)
    #
    #     for row in result:
    #         delete_query = f"DELETE FROM mydatabase.{table_name} WHERE tconst = '{row.tconst}'"
    #         session.execute(delete_query)
    #
    #     end_time = time.time()
    #     return end_time - start_time

    def test_time_for_delete(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata"
    ) -> float:
        start_time = time.time()
        session = self.connect()

        query = f"SELECT tconst FROM mydatabase.{table_name} LIMIT {record_amount}"
        result = session.execute(query)

        batch_size = 100
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        for i, row in enumerate(result, start=1):
            delete_query = f"DELETE FROM mydatabase.{table_name} WHERE tconst = '{row.tconst}'"
            batch.add(SimpleStatement(delete_query))
            if i % batch_size == 0:
                # Execute the batch after processing a batch size of delete queries
                session.execute(batch)
                batch.clear()
        # Execute any remaining statements in the last batch
        session.execute(batch)

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
                ['Documentary', 'Short']
            ]
    ) -> float:
        start_time = time.time()
        session = self.connect()

        query = f"SELECT tconst FROM mydatabase.{table_name} LIMIT {record_amount}"
        result = session.execute(query)

        batch_size = 100
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        for i, row in enumerate(result, start=1):
            # update_query = f"UPDATE mydatabase.{table_name} SET titleType = ?, primaryTitle = ?, originalTitle = ?, " \
            #                f"isAdult = ?, startYear = ?, endYear = ?, runtimeMinutes = ?, genres = ? WHERE tconst = ?"
            # session.execute(update_query, (
            #     values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], tconst
            # ))

            # query = f"INSERT INTO mydatabase.{table_name} (titleType, primaryTitle, originalTitle, isAdult, " \
            #         f"startYear, endYear, runtimeMinutes, genres) VALUES ('{values[0]}', '{values[1]}', '{values[2]}', " \
            #         f"'{values[3]}', '{values[4]}', '{values[5]}', '{values[6]}', '{values[7]}')"

            # update_query = f"UPDATE mydatabase.{table_name} SET titleType = %s, primaryTitle = %s, originalTitle = %s, " \
            #                f"isAdult = %s, startYear = %s, endYear = %s, runtimeMinutes = %s, genres = %s WHERE tconst = %s"
            #
            # values = (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], row.tconst)
            # update_query = update_query % values

            # update_query = f'UPDATE mydatabase.{table_name} SET titleType = \"{values[0]}\", primaryTitle = \"{values[1]}\", originalTitle = \"{values[2]}\", ' \
            #                f'isAdult = \"{values[3]}\", startYear = \"{values[4]}\", endYear = \"{values[5]}\", runtimeMinutes = \"{values[6]}\", genres = \"{values[7]}\" WHERE tconst = \"{row.tconst}\"'
            update_query = f"UPDATE mydatabase.{table_name} SET titleType = '{values[0]}', primaryTitle = '{values[1]}', originalTitle = '{values[2]}', " \
                           f"startYear = '{values[4]}', endYear = '{values[5]}', runtimeMinutes = '{values[6]}' WHERE tconst = '{row.tconst}'"

            batch.add(SimpleStatement(update_query))
            if i % batch_size == 0:
                # Execute the batch after processing a batch size of delete queries
                session.execute(batch)
                batch.clear()
        session.execute(batch)
        end_time = time.time()
        return end_time - start_time
    
    def test_time_for_max(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        """
        https://stackoverflow.com/questions/19370130/cassandra-cql-not-equal-operator-on-any-column
        """
        session = self.connect()
        start_time = time.time()
        query = f"SELECT {column_name} FROM {table_name}"
        result = session.execute(query)
 
        non_null_values = [row[0] for row in result if row[0] is not None and row[0] != r'\N']
        max_value = max(non_null_values) if non_null_values else None
        print(max_value)
 
        end_time = time.time()
        return end_time - start_time, max_value
 
    def test_time_for_min(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        session = self.connect()
        start_time = time.time()
        query = f"SELECT MIN({column_name}) FROM {table_name}"
        result = session.execute(query, control_connection_timeout = 100000)
        min_value = result.one()[0]
        print(min_value)
 
        end_time = time.time()
        return end_time - start_time, min_value