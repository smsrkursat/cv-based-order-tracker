import cv2
import numpy as np

class FoodDetector:
    def __init__(self, menu_items):
        self.menu_items = menu_items
        self.detected_items = []
        
    def detect_food(self, frame):
        """Basit renk tabanlı yemek tespiti simülasyonu"""
        detected = []
        color_ranges = {
            "sulu_yemek": ([0, 50, 50], [10, 255, 255]),    # Kırmızı
            "izgara": ([10, 50, 50], [20, 255, 255]),       # Kahverengi
            "corba": ([20, 50, 50], [30, 255, 255]),        # Turuncu
            "salata": ([50, 50, 50], [70, 255, 255]),       # Yeşil
            "tatli": ([30, 50, 50], [40, 255, 255])         # Sarı
        }
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for food_type, (lower, upper) in color_ranges.items():
            lower = np.array(lower)
            upper = np.array(upper)
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    detected.append({
                        "type": food_type,
                        "name": self.menu_items[food_type]["name"],
                        "price": self.menu_items[food_type]["price"],
                        "bbox": [x, y, w, h],
                        "confidence": 0.85
                    })
        return detected
