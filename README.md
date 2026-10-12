# Data Masking for PDPA — Python re

## รันในเครื่อง

## ไฟล์

- static/index.html: หน้าเว็บเรียก app.js
- static/app.js: รับ input, เรียก API, แสดง output, โหลดตัวอย่างและคัดลอก ไม่มี Regex สำหรับ masking
- masking.py: กฎเซ็นเซอร์ทั้ง 5 ประเภทด้วย Python re
- app.py: WSGI web app ให้บริการ HTML/JS และ API ไม่ใช้ framework เพิ่มเติม
- test_masking.py: unit tests และ API tests
- Dockerfile: ตัวเลือกสำหรับ deploy บนโฮสต์ที่รองรับ Docker
- EXPLANATION.md: อธิบายโค้ดและนโยบายกรณีพิเศษ

## ทดสอบ

```sh
python -m unittest -v
```

ทดสอบตัวอย่าง 20 กรณี การนับหลายรายการ และ API ตรวจ JSON/ขนาดข้อมูล/เส้นทางผิด

## Environment Variable

Windows PowerShell:

```powershell
$env:SOURCE_CODE_URL="https://github.com/DEKDDD/TOC"
python app.py
```

macOS/Linux:

```sh
SOURCE_CODE_URL="https://github.com/DEKDDD/TOC" python3 app.py
```

แทนค่าตัวอย่างด้วยข้อมูลจริง ปุ่ม Source Code จะแสดงเมื่อกำหนด URL repository บน github.com ไว้แล้ว

## ออนไลน์

ต้องใช้โฮสต์ที่รัน Python WSGI หรือ Docker ได้ หากนำ HTML ไปไว้ GitHub Pages อย่างเดียว ส่วน Python จะไม่ทำงาน

Docker สำหรับ production server (Gunicorn):

```sh
docker build -t pdpa-mask .
docker run --rm -p 8000:8000 -e SOURCE_CODE_URL="https://github.com/DEKDDD/TOC" pdpa-mask
```

โฮสต์กำหนด PORT ได้ ค่าเริ่มต้น 8000 ใช้ HTTPS เมื่อเผยแพร่
