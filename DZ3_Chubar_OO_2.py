from pymongo import MongoClient, errors
from bson.objectid import ObjectId

# Підключення до MongoDB Atlas
client = MongoClient('mongodb+srv://goitlearn:Chchchch1@cluster0.rirxhxh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['cat_database']
collection = db['cats']

# Створення бази даних та колекції з початковим документом
def create_initial_document():
    try:
        new_cat = {
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"]
        }
        collection.insert_one(new_cat)
        print("Initial document created successfully.")
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
    except errors.DuplicateKeyError as e:
        print(f"Duplicate key error: {e}")

# Функція для виведення всіх записів із колекції
def read_all_documents():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

# Функція для виведення інформації про кота за ім'ям
def read_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"No cat found with the name: {name}")
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

# Функція для оновлення віку кота за ім'ям
def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Cat's age updated successfully.")
        else:
            print(f"No cat found with the name: {name}")
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

# Функція для додавання нової характеристики до списку features кота за ім'ям
def add_feature_to_cat(name, feature):
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.matched_count > 0:
            print(f"Feature added successfully.")
        else:
            print(f"No cat found with the name: {name}")
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

# Функція для видалення запису за ім'ям тварини
def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Cat deleted successfully.")
        else:
            print(f"No cat found with the name: {name}")
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

# Функція для видалення всіх записів із колекції
def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"All cats deleted. Count: {result.deleted_count}")
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

# Приклади використання функцій
if __name__ == "__main__":
    # Створення початкового документа
    create_initial_document()
    
    # Виведення всіх записів
    print("All cats in the collection:")
    read_all_documents()

    # Виведення інформації про кота за ім'ям
    print("\nCat with the name 'barsik':")
    read_cat_by_name("barsik")

    # Оновлення віку кота за ім'ям
    print("\nUpdating age of 'barsik' to 4.")
    update_cat_age("barsik", 4)
    read_cat_by_name("barsik")

    # Додавання нової характеристики
    print("\nAdding new feature to 'barsik'.")
    add_feature_to_cat("barsik", "любит гратися з м'ячем")
    read_cat_by_name("barsik")

    # Видалення запису за ім'ям
    print("\nDeleting 'barsik'.")
    delete_cat_by_name("barsik")
    read_all_documents()

    # Видалення всіх записів
    print("\nDeleting all cats.")
    delete_all_cats()
    read_all_documents()
