# 1.将Python内置的模块（功能导入）
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def email_sen(str,semail,gemail,ssl,pwd):
# 2.构建邮件内容
    msg = MIMEText(str, "html", "utf-8")  # 内容
    msg["From"] = formataddr(["监测系统", semail])  # 自己名字/自己邮箱
    msg['to'] = gemail  # 目标邮箱
    msg['Subject'] = "上新提醒"  # 主题

# 3.发送邮件#"DGJBOKESOHGBACBQ"
    server = smtplib.SMTP_SSL(ssl)
    server.login(semail, pwd)  # 账户/授权码
# 自己邮箱、目标邮箱
    server.sendmail(semail, gemail, msg.as_string())
    server.quit()
