import smtplib
from email.mime.text import MIMEText
import random as r
import time as t
#QQ邮箱提供的SMTP服务器
mail_host = 'smtp.qq.com'
#服务器端口
port = 465
Email_ = ''
password = ''

def send_email(title,content,send_to):
    message = MIMEText(content,'plain','utf-8')
    message["From"] = Email_
    message['To'] = send_to
    message['Subject'] = title
    try:
        #注意第三个参数，设置了转码的格式(我不设的时候会报解码错误)
        smpt = smtplib.SMTP_SSL(mail_host, port, 'utf-8')
        smpt.login(send_by,password)
        smpt.sendmail(send_by, send_to,message.as_string())
        print("发送成功")
    except:
        print("发送失败")
# send_email(title,content,send_to)
def main(send_to):
    ran=r.randint(100000,999999)
    title = 'python QQ邮箱验证'
    content = str(ran)
    send_email(title,content,send_to)
    a=input("请输入验证码：")
    p=True
    while p:
        if a == "0":
            send_email(title,content,send_to)
            a=input("请输入验证码：")
        elif a != str(ran):
            a=input("验证码错误，请重新输入(重新发送按0):")
        else:
            p=False
            print("验证码正确，即将退出验证程序。")
            t.sleep(1)