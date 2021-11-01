import configparser
import os
import time
from pathlib import Path
import MeCab
import zmail
import schedule

from mailSendFunV2 import sendMail


# パソコン操作命令
def osController(command: str, commandPwd: str):
    # 需要自己变更密码
    # mecabを使っているので、cmdPwdは意味がないアルファベットを使ってください
    mailConfig = configparser.ConfigParser()
    mailConfig.read('userConfig.ini', encoding='utf-8')
    cmdPwd = mailConfig.get('mail', 'cmdpwd')
    if commandPwd == cmdPwd:
        if command == 'shutdown':
            # os.system('shutdown /s /t 30')
            print('shutdownまで30S')
            return '30s'
        elif command == 'restart':
            print('restartまで30S')
    else:
        return 'コマンドが存在しません'


# 日本語解析
def JPtoList(msg: str):
    mecab = MeCab.Tagger("-Owakati")
    JpStr = mecab.parse(msg)
    return JpStr.split()


# メールを解析し、自動返事する
def readAllMail():
    mailConfig = configparser.ConfigParser()
    mailConfig.read('userConfig.ini', encoding='utf-8')
    mailTextConfig = configparser.ConfigParser()
    mailTextConfig.read('mailText.ini', encoding='utf-8')
    mailUser = mailConfig.get('mail', 'mailUser')
    mailPwd = mailConfig.get('mail', 'mailPwd')
    cmdUser = mailConfig.get('mail', 'cmdUser')
    finalMailID = int(mailConfig.get('mail', 'finalMailID'))
    server = zmail.server(mailUser, mailPwd)
    mails = server.get_mails(start_index=finalMailID)
    for mail in mails:
        # HTMLのメールは識別できない可能性がある
        if len(mail['content_text']) != 0:
            body = mail['content_text'][0]
            msgBodyList = JPtoList(body)
            # パソコン操作
            if cmdUser in mail['From'] and msgBodyList[0] == 'コマンド':
                osMsg = osController(msgBodyList[1], msgBodyList[2])
                print(osMsg)
            else:
                # キーワード変更必要
                # mailText.iniに[ｘｘｘ]らしいものはキーワード、
                # default以外{'パスワード', 'キーワード１', 'キーワード２'}に書いてください
                # キーワードは日本語名詞と英語で書いてください
                keywordList = list(set(msgBodyList).intersection({'パスワード', '書いていません'}))
                if len(keywordList) != 0:
                    # キーワードを調べて、返事をする
                    for keyword in keywordList:
                        print('key:' + keyword)
                        title = mailTextConfig.get(keyword, 'title')
                        body = Path(mailTextConfig.get(keyword, 'bodyPath')).read_text(encoding='utf-8')
                        print('キーワード存在')
                        # sendMail(title, mail['From'], body)
                else:
                    title = mailTextConfig.get('default', 'title')
                    body = Path(mailTextConfig.get('default', 'bodyPath')).read_text(encoding='utf-8')
                    print('キーワード存在しません')
                    # sendMail(title, mail['From'], body)
        else:
            zmail.show(mail)
    # 更新finalMailID
    finalMailID = server.stat()[0]
    mailConfig.set('mail', 'finalMailID', str(finalMailID))
    mailConfig.write(open('userConfig.ini', 'w'))


if __name__ == '__main__':
    while True:
        readAllMail()
        # ２０分１回
        time.sleep(20 * 60)
