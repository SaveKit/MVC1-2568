# --- models/user.py ---
# Model สำหรับจัดการข้อมูลที่เกี่ยวกับ "ผู้ใช้ (User)"

from .database import load_data


class User:
    @staticmethod
    def find_by_username(username):
        """
        ฟังก์ชันสำหรับค้นหาผู้ใช้จาก username
        - ใช้สำหรับตอนล็อกอิน เพื่อหา user_id ที่ตรงกับ username ที่กรอกเข้ามา
        """
        all_data = load_data()
        for user in all_data["users"]:
            if user["username"].lower() == username.lower():
                return user
        return None
