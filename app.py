# --- app.py ---
# นี่คือ Controller และเป็นไฟล์หลักสำหรับรันเว็บแอปพลิเคชันของเรา
# เราจะใช้ Framework ที่ชื่อว่า Flask ในการสร้างเว็บ

import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, request, redirect, url_for, flash
from models.project import Project
from models.reward import Reward
from models.user import User

# สร้าง instance ของแอปพลิเคชัน Flask
load_dotenv()
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


# --- Route สำหรับดูรายละเอียดโครงการ ---
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


# --- Route สำหรับ Login ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # ถ้าเป็นการส่งฟอร์มเข้ามา
        username = request.form["username"]
        user = User.find_by_username(username)

        if user:
            # ถ้าหา user เจอ
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            flash(f'เข้าสู่ระบบสำเร็จในชื่อ {user["username"]}')  # ส่งข้อความ flash
            return redirect(url_for("index"))  # พาผู้ใช้กลับไปหน้าแรก
        else:
            # ถ้าหา user ไม่เจอ
            flash("Username ไม่ถูกต้อง")
            return redirect(url_for("login"))  # กลับไปหน้า login เหมือนเดิม

    # ถ้าเป็นการเปิดหน้าเว็บปกติ (GET) ให้แสดงฟอร์ม login
    return render_template("login.html")


# --- Route สำหรับ Logout ---
@app.route("/logout")
def logout():
    session.clear()  # ล้างข้อมูล session ทั้งหมด
    flash("ออกจากระบบเรียบร้อยแล้ว")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
