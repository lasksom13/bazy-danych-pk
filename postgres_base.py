import os
import subprocess
import time
import psycopg2
from pymongo import MongoClient
from psycopg2.extras import execute_values
from influxdb_base import InfluxDBClient
from time import sleep


def start_container(image, container_name, port):
    subprocess.run(['docker', 'run', '-d', '--name', container_name, '-p', f'{port}:5432', '-e', 'POSTGRES_PASSWORD=mysecretpassword', image])


def create_table():
    conn = psycopg2.connect(
        host='127.0.0.1',
        port=9005,
        database='postgres',
        user='postgres',
        password='mysecretpassword'
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE imdbdata (
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


def import_to_postgres(file_path):
    start_time = time.time()
    conn = psycopg2.connect(
        host='127.0.0.1',
        port=9005,
        database='postgres',
        user='postgres',
        password='mysecretpassword'
    )
    cursor = conn.cursor()
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip header line
        data = []
        for line in file:
            fields = line.strip().split('\t')
            fields[4] = fields[4] == '1'  # Convert isAdult field to boolean
            fields[8] = fields[8].split(',') if len(fields) > 8 else []  # Convert genres to list
            data.append(fields)
        execute_values(cursor, """
            INSERT INTO imdbdata (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
            VALUES %s
        """, data)
    conn.commit()
    cursor.close()
    conn.close()
    end_time = time.time()
    return end_time - start_time


def print_first_50_entries():
    conn = psycopg2.connect(
        host='127.0.0.1',
        port=9005,
        database='postgres',
        user='postgres',
        password='mysecretpassword'
    )
    cursor = conn.cursor()
    #cursor.execute("SELECT * FROM imdbdata LIMIT 50")
    cursor.execute(r"SELECT * FROM imdbdata WHERE endYear = '\N'")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()


def main():
    start_container('postgres:latest', 'postgres_db', 9005)
    sleep(5)
    create_table()
    time = import_to_postgres("title.basics.tsv/data_short.tsv")
    print(time)
    print_first_50_entries()


if __name__ == "__main__":
    main()
