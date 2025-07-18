from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient('mongodb://localhost:27017')
db = client['bgg_but']

menu_collection = db['menu_items']
orders_collection = db['orders']
waiters_collection = db['waiters']
tables_collection = db['tables']
images_collection = db['images']  # Yeni koleksiyon: Görüntü arşivi

def insert_sample_data():
    # Menü
    if menu_collection.count_documents({}) == 0:
        menu_collection.insert_many([
            {"_id": "sulu_yemek", "name": "Sulu Yemek", "price": 45, "color": "red"},
            {"_id": "izgara", "name": "Izgara", "price": 65, "color": "brown"},
            {"_id": "corba", "name": "Çorba", "price": 25, "color": "orange"},
            {"_id": "salata", "name": "Salata", "price": 35, "color": "green"},
            {"_id": "tatli", "name": "Tatlı", "price": 40, "color": "yellow"}
        ])
    # Garsonlar
    if waiters_collection.count_documents({}) == 0:
        waiters_collection.insert_many([
            {"_id": "1", "name": "Ahmet", "performance": 85, "orders_served": 12},
            {"_id": "2", "name": "Mehmet", "performance": 92, "orders_served": 15}
        ])
    # Masalar
    if tables_collection.count_documents({}) == 0:
        tables_collection.insert_many([
            {"_id": "1", "waiter_id": "1", "status": "occupied", "current_order": [], "total": 0},
            {"_id": "2", "waiter_id": "2", "status": "empty", "current_order": [], "total": 0}
        ])
