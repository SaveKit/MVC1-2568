# --- models/project.py ---
# นี่คือ Model ที่รับผิดชอบเฉพาะข้อมูลที่เกี่ยวกับ "โครงการ (Project)" เท่านั้น
# จะมีการเรียกใช้ฟังก์ชันจาก database.py เพื่อดึงข้อมูลมาทำงานต่อ

from .database import load_data


class Project:
    """
    คลาส Project นี้จะรวบรวมฟังก์ชันการทำงานทั้งหมดที่เกี่ยวกับโครงการ
    """

    @staticmethod
    def find_all():
        """
        ฟังก์ชันสำหรับดึงข้อมูล "โครงการทั้งหมด"
        - @staticmethod หมายความว่าเราสามารถเรียกใช้ฟังก์ชันนี้ได้เลยโดยไม่ต้องสร้าง object
          (เช่น เรียกใช้ Project.find_all() ได้เลย)
        - ขั้นตอนการทำงาน:
          1. เรียก load_data() เพื่อเอาข้อมูลทั้งหมดจาก data.json มา
          2. จากข้อมูลทั้งหมดนั้น เราสนใจแค่ส่วนที่เป็น 'projects'
          3. คืนค่า list ของโครงการทั้งหมดกลับไป
        """
        all_data = load_data()
        return all_data["projects"]

    @staticmethod
    def find_by_id(project_id):
        """
        ฟังก์ชันสำหรับค้นหาโครงการเดียวจาก ID ที่ระบุ
        - จะทำการวนลูปดูโครงการทั้งหมด ถ้าเจอ ID ที่ตรงกัน ก็จะคืนค่าโครงการนั้นออกไปทันที
        """
        all_data = load_data()
        for project in all_data["projects"]:
            if project["project_id"] == project_id:
                return project
        return None  # คืนค่า None ถ้าวนลูปจนจบแล้วยังไม่เจอโครงการที่ต้องการ
