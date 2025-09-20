# --- models/database.py ---
# นี่คือไฟล์ที่ทำหน้าที่เป็น "ตัวกลาง" ในการอ่านและเขียนข้อมูลจากไฟล์ data.json ของเรา
# เปรียบเสมือนคนเฝ้าคลังข้อมูล ใครจะเอาข้อมูลหรือจะเก็บข้อมูล ต้องผ่านคนนี้เท่านั้น

import json  # <-- library มาตรฐานของ Python สำหรับทำงานกับไฟล์ JSON

# กำหนดที่อยู่ของไฟล์ข้อมูลของเราให้เป็นตัวแปร เพื่อให้เรียกใช้ง่ายและแก้ไขสะดวก
DB_PATH = "data/data.json"


def load_data():
    """
    ฟังก์ชันสำหรับอ่านข้อมูลทั้งหมดจากไฟล์ JSON
    - ใช้ 'r' (read mode) เพื่ออ่านไฟล์
    - encoding='utf-8' เพื่อให้รองรับภาษาไทย
    - เมื่ออ่านไฟล์ได้ จะแปลงข้อมูล JSON เป็น Dictionary ของ Python แล้วส่งค่ากลับไป
    """
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # กรณีที่ไฟล์ data.json ยังไม่มีอยู่จริง จะคืนค่าเป็นโครงสร้างเปล่าๆ เพื่อไม่ให้โปรแกรมพัง
        return {"users": [], "projects": [], "reward_tiers": [], "pledges": []}


def save_data(data):
    """
    ฟังก์ชันสำหรับเขียนข้อมูลทั้งหมดกลับลงไปในไฟล์ JSON
    - ใช้ 'w' (write mode) เพื่อเขียนทับไฟล์เดิมทั้งหมด
    - indent=2 ทำให้ไฟล์ JSON ที่บันทึกถูกจัดรูปแบบสวยงาม อ่านง่าย
    - ensure_ascii=False เพื่อให้บันทึกภาษาไทยได้ถูกต้อง
    (ฟังก์ชันนี้เราจะยังไม่ได้ใช้ในขั้นตอนนี้ แต่เขียนเตรียมไว้สำหรับขั้นตอนถัดไป)
    """
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
