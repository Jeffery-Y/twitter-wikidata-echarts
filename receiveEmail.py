# -*- coding: utf-8 -*-

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib

# 输入邮件地址, 口令和POP3服务器地址:
email = 'getvpsresult@163.com' #'ymj.jeffrey@gmail.com'
password = 'yangmingjia'
pop3_server = 'pop.163.com'

def getEmailRequest():
    def decode_str(s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    server = poplib.POP3(pop3_server)
    # server.set_debuglevel(1)
    # 身份认证:
    server.user(email)
    server.pass_(password)
    # stat()返回邮件数量和占用空间:
    # print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    # print(mails)
    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    resp, lines, octets = server.retr(index)
    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)

    from_value = msg.get('From', '')
    from_hdr, from_addr = parseaddr(from_value)
    subject_value = msg.get('Sbuject', '')
    subject_value = decode_str(subject_value)

    if addr == '908210478@qq.com' and subject_value == 'request':
        # 可以根据邮件索引号直接从服务器删除邮件:
        server.dele(index)
        return True
    else:
        return False
    # 关闭连接:
    server.quit()
