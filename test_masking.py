import io
import json
import unittest
from app import application
from masking import mask_text

class MaskingTests(unittest.TestCase):
    def test_cases(self):
        cases = [
            ('1234-5678-9012-3456', 'XXXX-XXXX-XXXX-3456'),
            ('somchai.d@company.com', 's*******d@company.com'),
            ('093-245-7894', 'XXX-XXX-7894'),
            ('DOB:25/12/2549', 'DOB:XX/XX/25XX'),
            ('Address: 689 ซอยลาดกระบัง 19 ถนนลาดกระบัง แขวงลาดกระบัง เขตลาดกระบัง กรุงเทพฯ', 'Address: XXX ซอยลาดกระบัง 19 ถนนลาดกระบัง แขวงลาดกระบัง เขตลาดกระบัง กรุงเทพฯ'),
            ('Address: 123/45 ถนนตัวอย่าง ตำบลหนึ่ง อำเภอสอง นนทบุรี', 'Address: XXX ถนนตัวอย่าง ตำบลหนึ่ง อำเภอสอง นนทบุรี'),
            ('address:\t9-12 ถนน ก', 'address:\tXXX ถนน ก'),
            ('dob: 01/01/2540', 'dob: XX/XX/25XX'),
            ('25/12/2549', '25/12/2549'),
            ('บ้าน 689 ซอย 19', 'บ้าน 689 ซอย 19'),
            ('0932457894', '0932457894'),
            ('0093-245-7894', '0093-245-7894'),
            ('12345-5678-9012-3456', '12345-5678-9012-3456'),
            ('a@x.com ab@x.com abc@x.com', 'a@x.com ab@x.com a*c@x.com'),
            ('jane.doe+bank@example.co.th', 'j***********k@example.co.th'),
            ('<script>alert(1)</script>', '<script>alert(1)</script>'),
            ('Address:\n123 ถนน ก', 'Address:\n123 ถนน ก'),
            ('DOB:25/12/25499', 'DOB:25/12/25499'),
            ('', ''),
            ('ข้อความปกติ ราคา 123 บาท', 'ข้อความปกติ ราคา 123 บาท'),
        ]
        for original, expected in cases:
            with self.subTest(original=original):
                self.assertEqual(mask_text(original)['text'], expected)

    def test_multiple_and_counts(self):
        original = '1234-5678-9012-3456\nabc@example.com 093-245-7894 DOB:25/12/2549 Address: 689 ถนน ก 093-245-7894'
        result = mask_text(original)
        self.assertEqual(result['counts'], dict(credit=1, email=1, phone=2, dob=1, address=1))
        self.assertEqual(mask_text(result['text'])['text'], result['text'])

    def test_api(self):
        def request(path, method='GET', body=b'', content='application/json'):
            captured = []
            env = {'PATH_INFO':path, 'REQUEST_METHOD':method, 'CONTENT_TYPE':content,
                   'CONTENT_LENGTH':str(len(body)), 'wsgi.input':io.BytesIO(body)}
            result = b''.join(application(env, lambda status, headers: captured.append((status, dict(headers)))))
            return captured[0], result
        (status, headers), body = request('/api/mask', 'POST', json.dumps({'text':'093-245-7894'}).encode())
        self.assertEqual(status, '200 OK')
        self.assertEqual(json.loads(body)['text'], 'XXX-XXX-7894')
        self.assertEqual(headers['Cache-Control'], 'no-store')
        for payload in [b'{', b'[]', b'{"text":123}', b'null']:
            self.assertEqual(request('/api/mask','POST',payload)[0][0], '400 Bad Request')
        self.assertEqual(request('/api/mask','POST',b'{}','text/plain')[0][0], '415 Unsupported Media Type')
        self.assertEqual(request('/api/mask')[0][0], '405 Method Not Allowed')
        self.assertEqual(request('/missing')[0][0], '404 Not Found')
        self.assertEqual(request('/../app.py')[0][0], '404 Not Found')
        huge = json.dumps({'text':'x'*100001}).encode()
        self.assertEqual(request('/api/mask','POST',huge)[0][0], '413 Payload Too Large')
        for asset in ['/', '/app.js', '/api/config']:
            self.assertEqual(request(asset)[0][0], '200 OK')

if __name__ == '__main__':
    unittest.main(verbosity=2)
