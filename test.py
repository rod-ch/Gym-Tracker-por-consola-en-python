import csv
from collections import deque

datos = []

with open("ejercicios.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    datos = list(reader)
    for row in datos:
        with open("next_id.txt", "w") as text:
            text.write(f"{row['id']}\n")

