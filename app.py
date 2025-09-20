# --- app.py ---
# นี่คือ Controller และเป็นไฟล์หลักสำหรับรันเว็บแอปพลิเคชันของเรา
# เราจะใช้ Framework ที่ชื่อว่า Flask ในการสร้างเว็บ

import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, request, redirect, url_for, flash
from models.project import Project
from models.reward import Reward
from models.user import User
from models.pledge import Pledge

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
    - รับค่า query parameters จาก URL มาเพื่อใช้ในการค้นหา, กรอง, เรียงลำดับ
    """
    search = request.args.get("search")
    category = request.args.get("category")
    sort = request.args.get("sort")

    all_projects = Project.find_all(search_term=search, category=category, sort_by=sort)

    # (Optional) สร้าง list ของ category สำหรับ dropdown
    categories = Project.get_all_categories()

    return render_template(
        "projects_list.html", projects=all_projects, categories=categories
    )


# --- Route สำหรับดูรายละเอียดโครงการ ---
@app.route("/project/<project_id>", methods=["GET", "POST"])
def project_detail(project_id):
    """
    ฟังก์ชันสำหรับแสดงหน้ารายละเอียดของโครงการ และรับข้อมูลการสนับสนุน
    - รับ project_id ที่ผู้ใช้ร้องขอมาจาก URL
    - สั่งให้ Model ไปหาข้อมูลโครงการ (find_by_id) และข้อมูลรางวัล (find_by_project)
    - ส่งข้อมูลทั้งสองอย่างไปให้ View 'project_detail.html' แสดงผล
    """
    if request.method == "POST":
        # ตรวจสอบว่าผู้ใช้ล็อกอินหรือยัง
        if "user_id" not in session:
            flash("กรุณาล็อกอินก่อนทำการสนับสนุน")
            return redirect(url_for("login"))

        # ดึงข้อมูลจากฟอร์มที่ส่งมา
        user_id = session["user_id"]
        reward_id = request.form.get("reward_id")
        # แปลง reward_id เป็น integer ถ้ามีค่า, ถ้าไม่มี (เลือก "ไม่รับรางวัล") ให้เป็น None
        reward_id = int(reward_id) if reward_id else None

        try:
            amount = int(request.form.get("amount"))
        except (ValueError, TypeError):
            flash("กรุณากรอกจำนวนเงินเป็นตัวเลข")
            return redirect(url_for("project_detail", project_id=project_id))

        # สั่งให้ Pledge Model ทำการสร้างและตรวจสอบการสนับสนุน
        success, message = Pledge.create(user_id, project_id, amount, reward_id)
        flash(message)  # แสดงผลลัพธ์ให้ผู้ใช้ทราบ

        # redirect กลับมาที่หน้าเดิมเพื่อแสดงข้อมูลที่อัปเดตแล้ว
        return redirect(url_for("project_detail", project_id=project_id))

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


# --- Route สำหรับแสดงสถิติ ---
@app.route("/statistics")
def statistics():
    """
    ฟังก์ชันสำหรับแสดงหน้าสถิติ
    - สั่งให้ Pledge Model ไปนับจำนวนการสนับสนุนแต่ละประเภท
    - ส่งค่าที่นับได้ไปให้ View แสดงผล
    """
    successful = Pledge.count_successful()
    rejected = Pledge.count_rejected()
    return render_template(
        "statistics.html", successful_pledges=successful, rejected_pledges=rejected
    )


if __name__ == "__main__":
    app.run()
