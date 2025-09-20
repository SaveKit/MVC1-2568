# CS Crowdfunding Project

โปรเจกต์นี้เป็นระบบระดมทุนสำหรับโครงการ ซึ่งเป็นส่วนหนึ่งของการสอบ Exit Exam

## วิธีการติดตั้งและรันโปรเจกต์ (Setup Instructions)

1.  **Clone a repository:**

    ```bash
    git clone [your-github-repo-link]
    cd MVC1-2568
    ```

2.  **สร้างและเปิดใช้งาน Virtual Environment (แนะนำ):**

    ```bash
    # สำหรับ macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # สำหรับ Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **ติดตั้ง Dependencies ทั้งหมด:**
    ใช้ไฟล์ `requirements.txt` เพื่อติดตั้งทุกอย่างที่จำเป็นในคำสั่งเดียว

    ```bash
    pip install -r requirements.txt
    ```

4.  **ตั้งค่า Environment Variables:**
    คัดลอกไฟล์ `.env.example` ไปเป็น `.env` แล้วแก้ไขค่า `SECRET_KEY` ภายในไฟล์

    ```bash
    # สำหรับ macOS/Linux
    cp .env.example .env

    # สำหรับ Windows
    copy .env.example .env
    ```

5.  **รันแอปพลิเคชัน:**
    ```bash
    python app.py
    ```

แอปพลิเคชันจะรันอยู่ที่ `http://127.0.0.1:5000`
