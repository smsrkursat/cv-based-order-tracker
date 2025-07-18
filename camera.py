import cv2
import time
import threading

camera_active = False
current_frame = None

def camera_thread(food_detector, update_frame_callback):
    global camera_active, current_frame
    cap = cv2.VideoCapture(0)
    while camera_active:
        ret, frame = cap.read()
        if ret:
            detected_foods = food_detector.detect_food(frame)
            for food in detected_foods:
                x, y, w, h = food["bbox"]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{food['name']} - {food['price']}TL", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            current_frame = frame
            update_frame_callback(frame)
        time.sleep(0.1)
    cap.release()

def start_camera_thread(food_detector, update_frame_callback):
    global camera_active
    if not camera_active:
        camera_active = True
        thread = threading.Thread(target=camera_thread, args=(food_detector, update_frame_callback))
        thread.daemon = True
        thread.start()

def stop_camera_thread():
    global camera_active
    camera_active = False

def get_current_frame():
    global current_frame
    return current_frame
