import pandas as pd
import mysql.connector

df = pd.read_csv("../data/properties_clean.csv").fillna("")

connection = mysql.connector.connect(
    host="localhost",
    user="user_mydb",
    password="rootPASSWORD",
    database="my_db"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    URL VARCHAR(500),
    image VARCHAR(1000),
    property_type VARCHAR(50),
    price VARCHAR(50),
    location VARCHAR(255),
    rooms VARCHAR(20),
    bathrooms VARCHAR(20),
    square_meters VARCHAR(20),
    floor VARCHAR(50)
)
""")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO properties
        (title, URL, image, property_type, price, location, rooms, bathrooms, square_meters, floor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["title"],
        row["url"],
        row["image"],
        row["property_type"],
        row["price"],
        row["location"],
        row["rooms"],
        row["bathrooms"],
        row["square_meters"],
        row["floor"]
    ))

connection.commit()
cursor.close()
connection.close()