from os import getenv

import pymysql
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
USER = getenv("MYSQL_ROOT_USER")
PASSWORD = getenv("MYSQL_ROOT_PASSWORD")
HOST = getenv("HOST")
PORT = int(getenv("MYSQL_DOCKER_PORT"))
DATABASE = getenv("MYSQL_DATABASE")


# Fixture to create a database connection
@pytest.fixture(scope="module")
def db_connection():
    con = pymysql.connect(
        host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE
    )
    yield con
    con.close()


# Fixture to set up the database for testing
@pytest.fixture(scope="module")
def setup_database(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS test_table;")
    create_table_query = """
    CREATE TABLE test_table (
        id INT PRIMARY KEY,
        name VARCHAR(50)
    );
    """
    cursor.execute(create_table_query)
    db_connection.commit()
    cursor.close()
    yield
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS test_table;")
    db_connection.commit()
    cursor.close()


# Test for creating the table
def test_create_table(db_connection, setup_database):
    cursor = db_connection.cursor()
    cursor.execute("SHOW TABLES LIKE 'test_table';")
    result = cursor.fetchone()
    assert result is not None


# Test for inserting values into the table
def test_insert_values(db_connection):
    cursor = db_connection.cursor()
    insert_data_query = """
    INSERT INTO test_table (id, name) VALUES
        (1, 'John'),
        (2, 'Alice'),
        (3, 'Bob');
    """
    cursor.execute(insert_data_query)
    db_connection.commit()
    cursor.execute("SELECT COUNT(*) FROM test_table;")
    result = cursor.fetchone()
    assert result[0] == 3


# Test for dropping the table
def test_drop_table(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS test_table;")
    db_connection.commit()
    cursor.execute("SHOW TABLES LIKE 'test_table';")
    result = cursor.fetchone()
    assert result is None
