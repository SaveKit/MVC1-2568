# --- app.py ---
# นี่คือ Controller และเป็นไฟล์หลักสำหรับรันเว็บแอปพลิเคชันของเรา
# เราจะใช้ Framework ที่ชื่อว่า Flask ในการสร้างเว็บ

from flask import Flask, render_template  # <-- import เครื่องมือที่จำเป็นจาก Flask
from models.project import Project  # <-- import คลาส Project ที่เราสร้างไว้ใน Model

# สร้าง instance ของแอปพลิเคชัน Flask
app = Flask(__name__, template_folder="views")


# @app.route('/') คือการบอกว่า ถ้ามีคนเข้ามาที่หน้าแรกของเว็บ (URL: "/") ให้ทำฟังก์ชันข้างล่างนี้
@app.route("/")
def index():
    """
    ฟังก์ชันสำหรับจัดการหน้าแรก
    - ขั้นตอนการทำงาน:
      1. สั่งให้ Model (Project.find_all()) ไปดึงข้อมูลโครงการทั้งหมดมา
      2. เมื่อได้ข้อมูลมาแล้ว (เก็บในตัวแปร all_projects)
      3. สั่งให้ View (render_template) ไปแสดงผลที่ไฟล์ 'projects_list.html'
         พร้อมกับส่งข้อมูล all_projects ไปให้ View ใช้ (โดยตั้งชื่อตัวแปรใน View ว่า 'projects')
    """
    all_projects = Project.find_all()
    return render_template("projects_list.html", projects=all_projects)


# ส่วนนี้คือคำสั่งมาตรฐานเพื่อให้โปรแกรมสามารถรันได้เมื่อเราสั่ง `python app.py`
# debug=True จะทำให้เว็บ auto-reload เมื่อเราแก้ไขโค้ด ไม่ต้องปิดแล้วเปิดใหม่ทุกครั้ง
if __name__ == "__main__":
    app.run(debug=True)
