import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        dbname="task_management",
        user="postgres",
        password="Chchchch1",
        host="localhost",
        port="5432"
    )
    return conn

def execute_query(query, params=()):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def execute_update(query, params=()):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

# Отримати всі завдання, які ще не завершено
incomplete_tasks = execute_query("SELECT * FROM tasks WHERE status_id != %s", (1,))
print("Incomplete tasks:", incomplete_tasks)

# Видалити конкретне завдання за його id
def delete_task(task_id):
    execute_update("DELETE FROM tasks WHERE id = %s", (task_id,))

# Знайти користувачів з певною електронною поштою
def find_users_by_email(email_pattern):
    return execute_query("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))

# Оновити ім'я користувача
def update_user_name(user_id, new_name):
    execute_update("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id))

# Отримати кількість завдань для кожного статусу
task_counts_by_status = execute_query("SELECT status_id, COUNT(*) FROM tasks GROUP BY status_id")
print("Task counts by status:", task_counts_by_status)

# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_email_domain(domain):
    return execute_query("""
    SELECT tasks.* 
    FROM tasks 
    JOIN users ON tasks.user_id = users.id 
    WHERE users.email LIKE %s
    """, ('%@' + domain,))

# Отримати список завдань, що не мають опису
tasks_without_description = execute_query("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
print("Tasks without description:", tasks_without_description)

# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
users_tasks_in_progress = execute_query("""
SELECT users.*, tasks.* 
FROM users 
INNER JOIN tasks ON users.id = tasks.user_id 
WHERE tasks.status_id = 2  -- Припустимо, що 'in progress' має status_id 2
""")
print("Users and tasks in progress:", users_tasks_in_progress)

# Отримати користувачів та кількість їхніх завдань
users_task_counts = execute_query("""
SELECT users.id, users.fullname, COUNT(tasks.id) as task_count 
FROM users 
LEFT JOIN tasks ON users.id = tasks.user_id 
GROUP BY users.id, users.fullname
""")
print("Users task counts:", users_task_counts)

# Приклад отримання завдань певного користувача
user_id = 1
tasks = execute_query("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
print("Tasks for user_id 1:", tasks)

# Приклад вибору завдання за статусом
status_id = 1
tasks_by_status = execute_query("SELECT * FROM tasks WHERE status_id = %s", (status_id,))
print("Tasks by status_id 1:", tasks_by_status)

# Приклад оновлення статусу конкретного завдання
def update_task_status(task_id, new_status_id):
    execute_update("UPDATE tasks SET status_id = %s WHERE id = %s", (new_status_id, task_id))

# Оновлення статусу завдання
task_id = 1
new_status_id = 2
update_task_status(task_id, new_status_id)

# Приклад отримання списку користувачів, які не мають жодного завдання
users_without_tasks = execute_query("""
    SELECT * FROM users 
    WHERE id NOT IN (SELECT user_id FROM tasks)
""")
print("Users without tasks:", users_without_tasks)

# Приклад додавання нового завдання для конкретного користувача
def add_new_task(title, description, status_id, user_id):
    execute_update("""
        INSERT INTO tasks (title, description, status_id, user_id) 
        VALUES (%s, %s, %s, %s)
    """, (title, description, status_id, user_id))

# Додавання нового завдання
new_task = ("New Task Title", "Task Description", 1, user_id)
add_new_task(*new_task)

# Приклади виклику функцій:
# Видалення завдання з id 1
delete_task(1)

# Пошук користувачів з електронною поштою, яка містить 'example.com'
users = find_users_by_email('%@example.com')
print("Users with email domain 'example.com':", users)

# Оновлення імені користувача з id 1 на 'New Name'
update_user_name(1, 'New Name')

# Отримання завдань, призначених користувачам з доменом 'example.com'
tasks_by_domain = get_tasks_by_email_domain('example.com')
print("Tasks for email domain 'example.com':", tasks_by_domain)
