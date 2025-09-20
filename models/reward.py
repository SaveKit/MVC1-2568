# --- models/reward.py ---
# Model นี้ใช้สำหรับจัดการข้อมูลที่เกี่ยวกับ "รางวัล (Reward)" โดยเฉพาะ

from .database import load_data


class Reward:
    @staticmethod
    def find_by_project(project_id):
        """
        ฟังก์ชันสำหรับค้นหารางวัลทั้งหมดที่เป็นของโครงการที่ระบุ (จาก project_id)
        - จะทำการวนลูปดูรางวัลทั้งหมดในฐานข้อมูล แล้วเก็บเฉพาะอันที่ตรงเงื่อนไข
        """
        all_data = load_data()
        project_rewards = []
        for reward in all_data["reward_tiers"]:
            if reward["project_id"] == project_id:
                project_rewards.append(reward)
        return project_rewards
