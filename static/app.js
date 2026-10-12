'use strict';
// JavaScript controls the UI only. All masking happens in Python masking.py.
const input = document.getElementById('inputText');
const output = document.getElementById('outputText');
const status = document.getElementById('status');
const maskBtn = document.getElementById('maskBtn');
const copyBtn = document.getElementById('copyBtn');
let revision = 0;
let busy = false;
function resetOutput() {
  revision += 1;
  output.value = '';
  copyBtn.disabled = true;
  status.textContent = 'พร้อมเซ็นเซอร์ข้อความด้วย Python re';
}
async function processMasking() {
  if (busy) return;
  if (!input.value.trim()) { status.textContent = 'กรุณากรอกข้อความก่อน'; input.focus(); return; }
  busy = true;
  maskBtn.disabled = true;
  const submittedRevision = revision;
  status.textContent = 'กำลังประมวลผล…';
  try {
    const response = await fetch('/api/mask', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({text:input.value})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'ประมวลผลไม่สำเร็จ');
    if (submittedRevision !== revision) return;
    output.value = data.text;
    copyBtn.disabled = false;
    const total = Object.values(data.counts).reduce((sum, n) => sum + n, 0);
    status.textContent = `ประมวลผลแล้ว ตรวจพบข้อมูลที่ตรงรูปแบบ ${total} รายการ`;
  } catch (error) {
    if (submittedRevision === revision) status.textContent = `ไม่สำเร็จ: ${error.message} — ตรวจว่าเปิดเว็บผ่าน python app.py`;
  } finally {
    busy = false;
    maskBtn.disabled = false;
  }
}
async function copyToClipboard() {
  if (!output.value) return;
  try { await navigator.clipboard.writeText(output.value); status.textContent = 'คัดลอกผลลัพธ์แล้ว'; }
  catch { output.focus(); output.select(); status.textContent = 'เลือกผลลัพธ์แล้ว กด Ctrl+C หรือ Command+C เพื่อคัดลอก'; }
}
input.addEventListener('input', resetOutput);
maskBtn.addEventListener('click', processMasking);
copyBtn.addEventListener('click', copyToClipboard);
document.getElementById('sampleBtn').addEventListener('click', loadSample);
fetch('/api/config').then(response => response.json()).then(config => {
  if (!config.source_url) return;
  const link = document.getElementById('sourceLink');
  link.href = config.source_url;
  link.hidden = false;
  document.getElementById('sourceStatus').textContent = 'ดู Source Code ได้จากปุ่ม GitHub ด้านบน';
}).catch(() => { document.getElementById('sourceStatus').textContent = 'โหลดการตั้งค่า GitHub ไม่สำเร็จ'; });

function loadSample() {
  input.value = `ตัวอย่างบันทึกข้อมูลเพื่อการทดสอบ
------------------------------------------------
ข้อมูลลูกค้าคนที่ 1:
ชื่อ-นามสกุล: นายสมชาย ใจดี
อีเมล: somchai.d@company.com
เบอร์โทรศัพท์สำหรับติดต่อ: 093-245-7894
เลขบัตรเครดิตที่ใช้ผูกบัญชี: 1234-5678-9012-3456
DOB:25/12/2549
Address: 689 ซอยลาดกระบัง 19 ถนนลาดกระบัง แขวงลาดกระบัง เขตลาดกระบัง กรุงเทพฯ

ข้อมูลลูกค้าคนที่ 2:
ชื่อ-นามสกุล: นางสาวมาลี สีสด
อีเมล: malee_see@gmail.com
เบอร์โทรศัพท์สำหรับติดต่อ: 081-987-6543
เลขบัตรเครดิตที่ใช้ผูกบัญชี: 9876-5432-1098-7654
DOB:01/05/2530
Address: 12/34 หมู่ 5 ถนนรามคำแหง แขวงหัวหมาก เขตบางกะปิ กรุงเทพฯ`;
  resetOutput();
}
