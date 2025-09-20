# --- models/pledge.py ---
# Model สำหรับจัดการข้อมูลการสนับสนุน (Pledge) และตรรกะทางธุรกิจทั้งหมด

import uuid
from datetime import datetime
from .database import load_data, save_data


class Pledge:
    @staticmethod
    def create(user_id, project_id, amount, reward_id):
        """
        ฟังก์ชันหลักสำหรับสร้างการสนับสนุนใหม่ และตรวจสอบ Business Rules ทั้งหมด
        - จะคืนค่าเป็น tuple (boolean, message) เช่น (True, "สนับสนุนสำเร็จ!") หรือ (False, "จำนวนเงินไม่พอ")
        """
        all_data = load_data()

        # ค้นหาโครงการที่ต้องการสนับสนุน
        project = next(
            (p for p in all_data["projects"] if p["project_id"] == project_id), None
        )
        if not project:
            return (False, "ไม่พบโครงการที่ระบุ")

        # --- Business Rule 1: ตรวจสอบ Deadline ---
        # แปลง deadline string เป็น object datetime เพื่อเปรียบเทียบ
        deadline_date = datetime.strptime(project["deadline"], "%Y-%m-%d")
        if datetime.now() > deadline_date:
            # บันทึกเป็น rejected pledge ถ้่าโครงการหมดเวลาแล้ว
            Pledge._log_pledge(
                all_data, user_id, project_id, amount, reward_id, "rejected"
            )
            return (False, "โครงการนี้สิ้นสุดการระดมทุนแล้ว")

        # --- Business Rule 2: ตรวจสอบยอดเงินขั้นต่ำของรางวัล (ถ้าเลือก) ---
        selected_reward = None
        if reward_id:
            selected_reward = next(
                (r for r in all_data["reward_tiers"] if r["reward_id"] == reward_id),
                None,
            )
            if selected_reward and amount < selected_reward["min_amount"]:
                Pledge._log_pledge(
                    all_data, user_id, project_id, amount, reward_id, "rejected"
                )
                return (
                    False,
                    f"ยอดสนับสนุนต้องไม่ต่ำกว่า {selected_reward['min_amount']} บาท สำหรับรางวัลนี้",
                )

        # --- เมื่อผ่านทุกเงื่อนไข: บันทึกเป็น Successful Pledge ---
        # อัปเดตยอดเงินโครงการ
        project["current_amount"] += amount
        # ลดจำนวนรางวัล (ถ้ามี)
        if selected_reward and selected_reward["quantity_left"] > 0:
            selected_reward["quantity_left"] -= 1

        Pledge._log_pledge(
            all_data, user_id, project_id, amount, reward_id, "successful"
        )
        return (True, "ขอบคุณสำหรับการสนับสนุน!")

    @staticmethod
    def _log_pledge(all_data, user_id, project_id, amount, reward_id, status):
        """
        ฟังก์ชันช่วยสำหรับบันทึกข้อมูล pledge ลงใน data structure และ save ลงไฟล์
        """
        new_pledge = {
            "pledge_id": str(uuid.uuid4()),  # สร้าง ID ที่ไม่ซ้ำกัน
            "user_id": user_id,
            "project_id": project_id,
            "amount": amount,
            "reward_id": reward_id,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }
        all_data["pledges"].append(new_pledge)
        save_data(all_data)
