import smtplib
from email.mime.text import MIMEText
from email.header import Header


class mailClass:
    def __init__(self, mail_host, mail_user, mail_pass, sender):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender


if __name__ == '__main__':
    mailObj = mailClass("smtp.office365.com", "asberlhant@outlook.com", "your PWD", 'asberlhant@outlook.com')
    receivers = ['2537362680@qq.com']
    body = '''
    見えますか
    日本語のテスト
    '''
    message = MIMEText(body, 'plain', 'utf-8')
    subject = '2021/10/13 23:22测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP(mailObj.mail_host, 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(mailObj.mail_user, mailObj.mail_pass)
        smtpObj.sendmail(mailObj.sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
