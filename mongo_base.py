import os
import subprocess
import time
from pymongo import MongoClient
from time import sleep


# Function to create and start a Docker container
def start_container(image, container_name, port):
    subprocess.run(['docker', 'run', '-d', '--name', container_name, '-p', f'{port}:27017', image])


# Function to insert data into MongoDB
def import_to_mongodb(file_path):
    start_time = time.time()
    client = MongoClient('mongodb://localhost:9006/')
    db = client['imdb']
    collection = db['imdbdata']
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip header line
        for line in file:
            fields = line.strip().split('\t')
            document = {
                'tconst': fields[0],
                'titleType': fields[1],
                'primaryTitle': fields[2],
                'originalTitle': fields[3],
                'isAdult': fields[4] == '1',
                'startYear': fields[5],
                'endYear': fields[6],
                'runtimeMinutes': fields[7],
                'genres': fields[8].split(',') if len(fields) > 8 else []
            }
            collection.insert_one(document)
    client.close()
    end_time = time.time()
    return end_time - start_time


def print_first_50_entries():
    client = MongoClient('mongodb://localhost:9006/')
    db = client['imdb']
    collection = db['imdbdata']
    cursor = collection.find().limit(50)
    for document in cursor:
        print(document)
    client.close()


def main():
    start_container('mongo:latest', 'mongo_db', 9006)
    sleep(5)
    time = import_to_mongodb("title.basics.tsv/data_short.tsv")
    print(time)
    print_first_50_entries()


if __name__ == "__main__":
    main()