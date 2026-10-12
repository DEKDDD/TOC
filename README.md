# Data Masking for PDPA — Python re

ใช้ HTML/CSS, Tailwind, ฟอนต์, ไอคอน และข้อความตัวอย่าง ปรับเฉพาะการประมวลผลและสถานะการใช้งานให้เชื่อม Python backend

## รันในเครื่อง

1. ติดตั้ง Python 3.10 ขึ้นไป
2. แตก ZIP แล้วเปิด Terminal
3. รัน `python app.py` (หรือ `python3 app.py`)
4. เปิด http://127.0.0.1:8000
5. กดโหลดตัวอย่าง แล้วทำการเซ็นเซอร์ข้อมูล

ไม่ต้อง pip install สำหรับการรันในเครื่อง ห้ามดับเบิลคลิก HTML โดยตรงหรือเปิดด้วย Live Server แทน Python server เพราะจะไม่มี /api/mask

หน้าตายังคงใช้ Tailwind CDN, Google Fonts และ Font Awesome เหมือนต้นฉบับ จึงต้องมีอินเทอร์เน็ตเพื่อโหลดรูปแบบหน้าเว็บ การประมวลผล Regex รันใน Python ของเครื่องหรือเซิร์ฟเวอร์ที่เปิดแอป ไม่ได้ส่งข้อความไปบริการ CDN เหล่านี้

## ส่วนที่เปลี่ยน

| ส่วน | เดิม | ใหม่ |
|---|---|---|
| Regex | JavaScript /pattern/g และ text.replace | Python re.compile / re.sub |
| processMasking | เซ็นเซอร์ในเบราว์เซอร์ | fetch POST /api/mask แล้วแสดง data.text |
| หน้าตา | HTML + Tailwind เดิม | คงโครงสร้างและคลาสเดิม เพิ่มสถานะ |
| ปุ่มคัดลอก | document.execCommand | Clipboard API และเลือกข้อความเป็น fallback |
| Source Code | ลิงก์ GitHub สมมติ | รับ URL จริงจาก SOURCE_CODE_URL |
| การเปิดเว็บ | เปิดไฟล์ HTML | รัน Python แล้วเปิด localhost |

## ไฟล์

- static/index.html: หน้าเว็บเดิมที่แก้ให้เรียก app.js
- static/app.js: รับ input, เรียก API, แสดง output, โหลดตัวอย่างและคัดลอก ไม่มี Regex สำหรับ masking
- masking.py: กฎเซ็นเซอร์ทั้ง 5 ประเภทด้วย Python re
- app.py: WSGI web app ให้บริการ HTML/JS และ API ไม่ใช้ framework เพิ่มเติม
- test_masking.py: unit tests และ API tests
- Dockerfile: ตัวเลือกสำหรับ deploy บนโฮสต์ที่รองรับ Docker (ยังไม่ได้ build/deploy ในรอบนี้)
- EXPLANATION.md: อธิบายโค้ดและนโยบายกรณีพิเศษ

## ทดสอบ

```sh
python -m unittest -v
```

ทดสอบตัวอย่าง 20 กรณี การนับหลายรายการ และ API ตรวจ JSON/ขนาดข้อมูล/เส้นทางผิด

## ใส่ GitHub ของกลุ่ม

อัปโหลดโค้ดทั้งหมดในโฟลเดอร์นี้เข้า repository ก่อน จากนั้นตั้ง environment variable เป็น URL จริง

Windows PowerShell:

```powershell
$env:SOURCE_CODE_URL="https://github.com/YOUR_USERNAME/YOUR_REPOSITORY"
python app.py
```

macOS/Linux:

```sh
SOURCE_CODE_URL="https://github.com/YOUR_USERNAME/YOUR_REPOSITORY" python3 app.py
```

แทนค่าตัวอย่างด้วยข้อมูลจริง ปุ่ม Source Code จะแสดงเมื่อกำหนด URL repository บน github.com ไว้แล้ว

## ออนไลน์

ต้องใช้โฮสต์ที่รัน Python WSGI หรือ Docker ได้ หากนำ HTML ไปไว้ GitHub Pages อย่างเดียว ส่วน Python จะไม่ทำงาน

Docker สำหรับ production server (Gunicorn):

```sh
docker build -t pdpa-mask .
docker run --rm -p 8000:8000 -e SOURCE_CODE_URL="https://github.com/YOUR_USERNAME/YOUR_REPOSITORY" pdpa-mask
```

โฮสต์กำหนด PORT ได้ ค่าเริ่มต้น 8000 ใช้ HTTPS เมื่อเผยแพร่ ยังไม่ได้สร้าง GitHub repository หรือเว็บออนไลน์ให้ในไฟล์งานนี้

ก่อนส่งต้องมี URL เว็บ, ลิงก์ Source Code จริงบนหน้าเว็บ, คลิป YouTube ไม่เกิน 10 นาที และหน้าที่สมาชิกตามโจทย์
