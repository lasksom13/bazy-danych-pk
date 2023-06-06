import subprocess
import time
from pymongo import MongoClient
from time import sleep
from abstract import BaseCommands
import typing as tp
import os


class MongoDB(BaseCommands):
    def __init__(
            self,
            host: str = "127.0.0.1",
            container_name: str = "mongo_db",
            image: str = "mongo:latest",
            port: int = 9006
    ):
        self._host = host
        self._container_name = container_name
        self._image = image
        self._port = port

    def start_database(
            self
    ) -> None:
        """
        run docker image of postgres database
        """
        try:
            subprocess.run(['docker', 'run', '-d', '--name', self._container_name, '-p', f'{self._port}:27017', self._image])
        except Exception as e:
            print("Error when start_database")
            print("error type: ", type(e))
            print(str(e))

    def connect(self) -> MongoClient:
        client: MongoClient = MongoClient(host=self._host, port=self._port)
        return client

    def create_table(
            self,
            table_name: str = "imdbdata"
    ) -> None:
        client = self.connect()
        db = client['mydatabase']
        collection = db[table_name]
        collection.create_index("tconst", unique=True)
        client.close()

    def drop_table(
            self,
            table_name: str = "imdbdata"
    ) -> None:
        client = self.connect()
        db = client['mydatabase']
        collection = db[table_name]
        collection.drop()
        client.close()
        pass

    def test_time_for_insert(
        self,
        record_amount: int = 10000,
        table_name: str = "imdbdata",
        values: tp.Optional[tp.List] = None
    ) -> float:
        """
        Insert records into MongoDB collection
        """
        start_time = time.time()
        client = self.connect()
        db = client['mydatabase']
        collection = db[table_name]

        with open("." + os.path.sep + "title.basics.tsv" + os.path.sep + "data.tsv", 'r', encoding='utf-8') as file:
            next(file)  # Skip header line
            records = []
            iterator = 0
            for line in file:
                if iterator >= record_amount:
                    break
                fields = line.strip().split('\t')
                fields[4] = fields[4] == '1'  # Convert isAdult field to boolean
                fields[8] = fields[8].split(',') if len(fields) > 8 else []  # Convert genres to list
                record = {
                    "tconst": fields[0],
                    "titleType": fields[1],
                    "primaryTitle": fields[2],
                    "originalTitle": fields[3],
                    "isAdult": fields[4],
                    "startYear": fields[5],
                    "endYear": fields[6],
                    "runtimeMinutes": fields[7],
                    "genres": fields[8]
                }
                records.append(record)
                iterator += 1

            collection.insert_many(records)

        client.close()
        end_time = time.time()
        return end_time - start_time

    def test_time_for_delete(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata"
    ) -> float:
        start_time = time.time()
        client = self.connect()
        db = client["mydatabase"]
        collection = db[table_name]
        documents = collection.find().limit(record_amount)
        for document in documents:
            primary_key = document["_id"]
            collection.delete_one({"_id": primary_key})

        client.close()
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
        client = self.connect()
        db = client["mydatabase"]
        collection = db[table_name]
        primary_key_column = "_id"
        documents = collection.find().limit(record_amount)
        update_query = {
            "$set": {
                "titleType": values[0],
                "primaryTitle": values[1],
                "originalTitle": values[2],
                "isAdult": values[3],
                "startYear": values[4],
                "endYear": values[5],
                "runtimeMinutes": values[6],
                "genres": values[7]
            }
        }
        for document in documents:
            primary_key_value = document["_id"]
            collection.update_one({"_id": primary_key_value}, update_query)

        client.close()
        end_time = time.time()
        return end_time - start_time

    def get_record_amount(
            self,
            table_name: str = "imdbdata",
    ) -> int:
        client = self.connect()
        db = client['mydatabase']
        collection = db[table_name]
        count = collection.count_documents({})
        client.close()
        return count

    def list_tables(self) -> tp.List[str]:
        """
        List the collections in MongoDB database
        """
        client = self.connect()
        db = client['mydatabase']
        collections = db.list_collection_names()
        client.close()
        return collections

    def test_time_for_record_amount_with_word(
            self,
            field_name: str,
            search_word: str,
            table_name: str = "imdbdata"
    ) -> float:
        pass

    def test_time_for_user_query(
            self,
            # query: str = "SELECT * FROM imdbdata LIMIT 50"
            query: str = "50"
    ) -> tp.Tuple[float, tp.List]:
        """
        Ten endpoint zwraca domyślnie 50 wpisów tylko
            (na potrzeby weryfikacji -> ignoruje totalnie query zamiast niego bierze ile rekordów wypisać

        Mongodb chyba nie wspiera query jako długiego stringa i trzeba zapytanie robić jako takie coś
                query = [
            {"$match": {"genre": "Action"}},
            {"$sort": {"release_date": -1}},
            {"$project": {"title": 1, "release_date": 1, "_id": 0}}
        ]
        :return: tuple (time to execute, result_of_query as list)
        """
        start_time = time.time()
        client = self.connect()
        db = client["mydatabase"]
        collection = db["imdbdata"]

        pipeline = [
            {"$limit": int(query)},
            {"$match": {}}
        ]

        result = list(collection.aggregate(pipeline))
        client.close()
        end_time = time.time()
        for row in result:
            print(row)
        return end_time - start_time, result

    def test_time_for_max(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        start_time = time.time()
        client = self.connect()
        db = client["mydatabase"]
        collection = db[table_name]

        max_value = collection.aggregate([
            {"$match": {column_name: {"$ne": None, "$ne": r"\N"}}},
            {"$group": {"_id": None, "max_value": {"$max": f"${column_name}"}}}
        ]).next()["max_value"]
        print(max_value)
        client.close()
        end_time = time.time()
        return end_time - start_time, max_value

    def test_time_for_min(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        start_time = time.time()
        client = self.connect()
        db = client["mydatabase"]
        collection = db[table_name]

        min_value = collection.aggregate([
            {"$match": {column_name: {"$ne": None, "$ne": r"\N"}}},
            {"$group": {"_id": None, "min_value": {"$min": f"${column_name}"}}}
        ]).next()["min_value"]
        print(min_value)
        client.close()
        end_time = time.time()
        return end_time - start_time, min_value

    def test_time_for_sorting(
            self,
            column_name: str = "runtimeMinutes",
            table_name: str = "imdbdata"
    ) -> tuple:
        start_time = time.time()
        client = self.connect()
        db = client["mydatabase"]
        collection = db[table_name]
        cursor = collection.find().sort(column_name)
        rows = list(cursor)
        for row in rows:
            print(row)
        client.close()
        end_time = time.time()
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
        client = self.connect()
        db = client["mydatabase"]
        collection = db[table_name]
        pipeline = [
            {"$match": {column_name: {"$ne": None, "$not": {"$eq": r"\N"}}}},
            {"$group": {"_id": None, "median": {"$avg": {"$toDouble": f"${column_name}"}}}}
        ]
        result = list(collection.aggregate(pipeline))
        median = result[0]["median"] if result else None
        client.close()
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
        client = self.connect()
        db = client["mydatabase"]
        collection = db[table_name]

        pipeline = [
            {"$match": {column_name: {"$ne": None, "$not": {"$eq": r"\N"}}}},
            {"$group": {"_id": f"${column_name}", "count": {"$sum": 1}}}
        ]

        result = list(collection.aggregate(pipeline))
        rows = [(item["_id"], item["count"]) for item in result]

        client.close()
        end_time = time.time()

        return end_time - start_time, rows


if __name__ == "__main__":
    # main()
    print("start")
    ins = MongoDB()
