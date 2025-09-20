# --- app.py ---
# นี่คือ Controller และเป็นไฟล์หลักสำหรับรันเว็บแอปพลิเคชันของเรา
# เราจะใช้ Framework ที่ชื่อว่า Flask ในการสร้างเว็บ

import os
from dotenv import load_dotenv
from flask import Flask, render_template
from models.project import Project
from models.reward import Reward

# สร้าง instance ของแอปพลิเคชัน Flask
app = Flask(__name__, template_folder="views")

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]


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


@app.route("/project/<project_id>")
def project_detail(project_id):
    """
    ฟังก์ชันสำหรับแสดงหน้ารายละเอียดของโครงการ
    - รับ project_id ที่ผู้ใช้ร้องขอมาจาก URL
    - สั่งให้ Model ไปหาข้อมูลโครงการ (find_by_id) และข้อมูลรางวัล (find_by_project)
    - ส่งข้อมูลทั้งสองอย่างไปให้ View 'project_detail.html' แสดงผล
    """
    project = Project.find_by_id(project_id)
    rewards = Reward.find_by_project(project_id)
    return render_template("project_detail.html", project=project, rewards=rewards)


if __name__ == "__main__":
    app.run()
