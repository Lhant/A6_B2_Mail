import poplib
import os
import MeCab
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


def osController(command: str, commandPwd: str):
    # 需要自己变更密码
    # mecabを使っているので、commandPwdは意味がないアルファベットを使ってください
    if commandPwd == 'qweasd':
        if command == 'shutdown':
            # os.system('shutdown /s /t 30')
            print('shutdownまで30S')
            return '30s'
        elif command == 'restart':
            print('restartまで30S')
    else:
        return '错误指令'


def JPtoList(msg: str):
    mecab = MeCab.Tagger("-Owakati")
    JpStr = mecab.parse(msg)
    return JpStr.split()


def getBodyContent(messageObject):
    """获取邮件正文内容"""
    msgBodyContents = []
    if messageObject.is_multipart():  # 判断邮件是否由多个部分构成
        messageParts = messageObject.get_payload()  # 获取邮件附载部分
        for messagePart in messageParts:
            bodyContent = decodeBody(messagePart)
            if bodyContent:
                msgBodyContents.append(bodyContent)
    else:
        bodyContent = decodeBody(messageObject)
        if bodyContent:
            msgBodyContents.append(bodyContent)
    return msgBodyContents


def decodeMsgHeader(header):
    """
    解码头文件
    :param header: 需解码的内容
    :return:
    """
    value, charset = decode_header(header)[0]
    if charset:
        value = value.decode(charset)
    return value


def decodeBody(msgPart):
    """
    解码内容
   :param msgPart: 邮件某部分
    """
    contentType = msgPart.get_content_type()  # 判断邮件内容的类型,text/html
    textContent = ""
    if contentType == 'text/plain' or contentType == 'text/html':
        content = msgPart.get_payload(decode=True)
        charset = msgPart.get_charset()
        if charset is None:
            contentType = msgPart.get('Content-Type', '').lower()
            position = contentType.find('charset=')
            if position >= 0:
                charset = contentType[position + 8:].strip()
        if charset:
            textContent = content.decode(charset)
    return textContent


if __name__ == '__main__':
    """POP的服务器信息"""
    popHost = 'outlook.office365.com'
    userAdr = 'asberlhant@outlook.com'
    userPwd = 'your PWD'

    """ 创建POP3对象，添加用户名和密码"""
    pop3Server = poplib.POP3_SSL(popHost, '995')
    pop3Server.user(userAdr)
    pop3Server.pass_(userPwd)

    """获取邮件数量和占用空间"""
    messageCount, mailboxSize = pop3Server.stat()

    """获取邮件请求返回状态码、每封邮件的字节大小(b'第几封邮件 此邮件字节大小')、"""
    response, msgNumOctets, octets = pop3Server.list()

    """ 获取邮件的邮件对象【第一封邮件的编号为1，而不是0】"""
    msgNumber = len(msgNumOctets)  # 最新邮件
    print(msgNumber)
    # 获取第msgIndex封邮件的信息,最后一封，后续需要改进
    response, msgLines, octets = pop3Server.retr(msgNumber)
    # msgLines中为该邮件的每行数据,先将内容连接成字符串，再转化为email.message.Message对象
    msgLinesToStr = b"\r\n".join(msgLines).decode("utf8", "ignore")
    messageObject = Parser().parsestr(msgLinesToStr)
    # print(messageObject)
    '''获取时间'''
    msgDate = messageObject["date"]
    print(msgDate)
    '''获取用户名'''
    senderContent = messageObject["From"]
    # parseaddr()函数返回的是一个元组(realname, emailAddress)
    senderRealName, senderAdr = parseaddr(senderContent)
    # 将加密的名称进行解码
    senderRealName = decodeMsgHeader(senderRealName)
    print(senderRealName)
    print(senderAdr)
    # 获取邮件主题
    msgHeader = messageObject["Subject"]
    # 对头文件进行解码
    msgHeader = decodeMsgHeader(msgHeader)
    print(msgHeader)

    # 获取正文

    """获取邮件正文内容"""
    msgBodyContents = getBodyContent(messageObject)
    print(msgBodyContents[0])
    # print(msgBodyContents[0].split()[0], msgBodyContents[0].split()[1])
    # print(senderAdr)
    '''发信人邮件，操作种类，操作指令，操作密码'''
    msgBodyList = JPtoList(msgBodyContents[0])
    print(msgBodyList)
    if senderAdr == '2537362680@qq.com' and msgBodyList[0] == 'コマンド':
        osMsg = osController(msgBodyList[1], msgBodyList[2])
        print(osMsg)
    else:
        print('自动回复还没写')

    """ 终止POP3服务"""
    pop3Server.quit()
