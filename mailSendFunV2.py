import configparser
import zmail
from datetime import datetime
from pathlib import Path
import re


def sendMail(title, receivers, body):
    mailConfig = configparser.ConfigParser()
    mailConfig.read('userConfig.ini', encoding='utf-8')
    mailUser = mailConfig.get('mail', 'mailUser')
    mailPwd = mailConfig.get('mail', 'mailPwd')
    server = zmail.server(mailUser, mailPwd)
    # 正则匹配邮箱
    # メールアドレスを探し出す
    if re.findall('<(.*?)>', receivers):
        receivers = re.findall('<(.*?)>', receivers)
    try:
        server.send_mail(receivers, {'subject': title, 'content_html': body})
        print("メール送信成功")
    except:
        fp = Path('mail.log')
        if not fp.exists():
            fp.write_text(data='ユーザー' + receivers + "\n" + str(datetime.now()) + '送信失敗', encoding='utf-8')
            print('送信失敗mail.logを確認してください')
        else:
            log = fp.read_text(encoding='utf-8')
            fp.write_text(log + "\n" + 'ユーザー　' + receivers + "\n　" + str(datetime.now()) + '　に送信失敗',
                          encoding='utf-8')
            print('送信失敗mail.logを確認してください')


