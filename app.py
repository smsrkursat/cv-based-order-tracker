from flask import Flask, render_template, jsonify, request
from datetime import datetime
from database import menu_collection, orders_collection, waiters_collection, tables_collection, images_collection, insert_sample_data
from food_detector import FoodDetector
from camera import start_camera_thread, stop_camera_thread, get_current_frame
from utils import frame_to_base64

app = Flask(__name__)

# Uygulama başlarken örnek verileri ekle
insert_sample_data()

# Menü verisini MongoDB'den çek
MENU_ITEMS = {item['_id']: item for item in menu_collection.find()}
food_detector = FoodDetector(MENU_ITEMS)

# Kamera frame güncelleme callback'i
def update_frame_callback(frame):
    pass  # Şimdilik gerek yok, ileride log veya başka işlem eklenebilir

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_camera')
def start_camera():
    start_camera_thread(food_detector, update_frame_callback)
    return jsonify({"status": "started"})

@app.route('/stop_camera')
def stop_camera():
    stop_camera_thread()
    return jsonify({"status": "stopped"})

@app.route('/get_frame')
def get_frame():
    frame = get_current_frame()
    if frame is not None:
        frame_data = frame_to_base64(frame)
        return jsonify({"frame": frame_data})
    return jsonify({"frame": None})

@app.route('/detect_food/<table_id>')
def detect_food(table_id):
    frame = get_current_frame()
    if frame is not None:
        detected_foods = food_detector.detect_food(frame)
        table = tables_collection.find_one({"_id": table_id})
        if table:
            tables_collection.update_one({"_id": table_id}, {"$set": {
                "current_order": detected_foods,
                "total": sum(food["price"] for food in detected_foods),
                "status": "occupied"
            }})
        # Görüntü ve tespit edilen yemekleri arşivle
        images_collection.insert_one({
            "table_id": table_id,
            "timestamp": datetime.now().isoformat(),
            "detected_foods": detected_foods,
            "image_data": frame_to_base64(frame)
        })
        return jsonify({
            "detected_foods": detected_foods,
            "total": sum(food["price"] for food in detected_foods),
            "table_id": table_id
        })
    return jsonify({"detected_foods": [], "total": 0})

@app.route('/get_image_archive')
def get_image_archive():
    # Son 20 arşiv kaydını getir
    images = list(images_collection.find().sort("timestamp", -1).limit(20))
    for img in images:
        img["_id"] = str(img["_id"])
    return jsonify(images)

@app.route('/clear_table/<table_id>')
def clear_table(table_id):
    table = tables_collection.find_one({"_id": table_id})
    if table:
        order_record = {
            "table_id": table_id,
            "waiter_id": table["waiter_id"],
            "items": table["current_order"],
            "total": table["total"],
            "timestamp": datetime.now().isoformat()
        }
        orders_collection.insert_one(order_record)
        tables_collection.update_one({"_id": table_id}, {"$set": {
            "current_order": [],
            "total": 0,
            "status": "empty"
        }})
        return jsonify({"status": "cleared", "order": order_record})
    return jsonify({"status": "error"})

@app.route('/get_tables')
def get_tables():
    tables = {t['_id']: {k: v for k, v in t.items() if k != '_id'} for t in tables_collection.find()}
    return jsonify(tables)

@app.route('/get_waiters')
def get_waiters():
    waiters = {w['_id']: {k: v for k, v in w.items() if k != '_id'} for w in waiters_collection.find()}
    return jsonify(waiters)

@app.route('/get_reports')
def get_reports():
    today = datetime.now().date()
    daily_orders = [o for o in orders_collection.find() if datetime.fromisoformat(o["timestamp"]).date() == today]
    waiters = {w['_id']: w for w in waiters_collection.find()}
    waiter_performance = {}
    for waiter_id, waiter in waiters.items():
        waiter_orders = [o for o in orders_collection.find({"waiter_id": waiter_id})]
        total_revenue = sum(o["total"] for o in waiter_orders)
        waiter_performance[waiter_id] = {
            "name": waiter["name"],
            "orders_count": len(waiter_orders),
            "total_revenue": total_revenue,
            "performance": waiter["performance"]
        }
    product_stats = {}
    for order in orders_collection.find():
        for item in order["items"]:
            item_type = item["type"]
            if item_type not in product_stats:
                product_stats[item_type] = {
                    "name": item["name"],
                    "count": 0,
                    "revenue": 0
                }
            product_stats[item_type]["count"] += 1
            product_stats[item_type]["revenue"] += item["price"]
    return jsonify({
        "daily_orders": daily_orders,
        "waiter_performance": waiter_performance,
        "product_stats": product_stats,
        "total_orders": orders_collection.count_documents({})
    })

@app.route('/simulate_order/<table_id>')
def simulate_order(table_id):
    import random
    menu_items = {item['_id']: item for item in menu_collection.find()}
    food_types = list(menu_items.keys())
    selected_foods = random.sample(food_types, random.randint(1, 3))
    simulated_order = []
    total = 0
    for food_type in selected_foods:
        food_info = menu_items[food_type]
        simulated_order.append({
            "type": food_type,
            "name": food_info["name"],
            "price": food_info["price"],
            "bbox": [100, 100, 150, 150],
            "confidence": 0.9
        })
        total += food_info["price"]
    table = tables_collection.find_one({"_id": table_id})
    if table:
        tables_collection.update_one({"_id": table_id}, {"$set": {
            "current_order": simulated_order,
            "total": total,
            "status": "occupied"
        }})
    return jsonify({
        "detected_foods": simulated_order,
        "total": total,
        "table_id": table_id
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)