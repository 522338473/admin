import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from .base import BaseMessage



class Email(BaseMessage):
    def __init__(self):
        self.email = "522338473@qq.com"
        self.user = "张建平"
        self.pwd = "yldhapaljlvrbhgg"
    def send(self,subject,body,to,name):
        msg = MIMEText(body, 'plain', 'utf-8')  # 发送内容
        msg['From'] = formataddr([self.user, self.email])  # 发件人
        msg['To'] = formataddr([name, to])  # 收件人
        msg['Subject'] = subject  # 主题

        server = smtplib.SMTP_SSL("smtp.qq.com",465)
        server.login(self.email,self.pwd)
        server.sendmail(self.email,[to,],msg.as_string())
        server.quit()






