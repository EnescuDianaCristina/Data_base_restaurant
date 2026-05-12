import random
from faker import Faker
from app.db import run_update, run_select

fake = Faker()

NUM_USERS = 80
NUM_PRODUCTS = 120
NUM_RETETE = 400

print("Cream user admin fix")

existing = run_select(
    "SELECT id FROM users WHERE username = %s",
    ("admin",)
)

if not existing:
    run_update(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s);",
        ("admin", "admin123")
    )

print("Generam utilizatori random cu parole simple")

simple_passwords = [
    "ananas",
    "parola123",
    "qwerty",
    "qwerty2024",
    "student123",
    "password",
    "abc123",
    "test123",
    "letmein",
    "maria2024"
]

for _ in range(NUM_USERS):
    username = fake.user_name() + str(random.randint(1, 999))
    password = random.choice(simple_passwords)

    run_update(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s);",
        (username, password)
    )

print("Generam ingrediente")

tipuri_de_ingrediente = ["lactate", "legume", "carne"]
list_ingrediente = ["pui", "porc", "vita", "morcovi", "rosii", "castraveti", "lapte", "branza"]

for i in range(1, NUM_PRODUCTS + 1):
    tip_de_ingredient = random.choice(tipuri_de_ingrediente)
    nume = random.choice(list_ingrediente)

    run_update(
        "INSERT INTO ingrediente (nume_ingredient, tip_ingredient) VALUES (%s, %s);",
        (nume, tip_de_ingredient)
    )


print("Initializam stoc")

ingredient_ids = run_select("SELECT id FROM ingrediente;")

stock_tracker = {}

for (ingredient_id,) in ingredient_ids:
    qty = random.randint(20, 200)
    stock_tracker[ingredient_id] = qty

    run_update(
        "INSERT INTO stoc (id_ingredient, nr_ingrediente) VALUES (%s, %s);",
        (ingredient_id, qty)
    )

print("Generam retete")

list_denumire = ["dulce", "sarat", "romanesc", "de provincie", "ca la mama acasa", "special", "studentesc", "a la inginer"]


for _ in range(NUM_RETETE):
    ingredient_id = random.choice(list(stock_tracker.keys()))
    current_stock = stock_tracker[ingredient_id]

    if current_stock > 0:
        nume = f"{random.choice(list_ingrediente)} {random.choice(list_denumire)}"
        reteta = f"{random.choice(list(stock_tracker.keys()))}, {random.choice(list(stock_tracker.keys()))}, {random.choice(list(stock_tracker.keys()))}"
        run_update(
            "INSERT INTO retete (nume_reteta, id_ingrediente_reteta) VALUES (%s, %s);",
            (nume, reteta)
        )

print("Date generate corect")
