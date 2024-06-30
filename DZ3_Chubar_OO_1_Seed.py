import psycopg2
from faker import Faker

# Підключення до бази даних
conn = psycopg2.connect(
    dbname="task_management",
    user="postgres",
    password="Chchchch1",  # Вкажіть ваш пароль
    host="localhost"
)
cur = conn.cursor()

# Ініціалізація Faker
fake = Faker()

# Додавання випадкових користувачів
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

# Отримання всіх статусів
cur.execute("SELECT id FROM status")
status_ids = [row[0] for row in cur.fetchall()]

# Додавання випадкових завдань
for _ in range(30):
    title = fake.sentence(nb_words=6)
    description = fake.text()
    status_id = fake.random.choice(status_ids)
    user_id = fake.random.randint(1, 10)  # Припускаємо, що у нас є 10 користувачів
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (title, description, status_id, user_id))

# Фіксація змін та закриття з'єднання
conn.commit()
cur.close()
conn.close()

