# -*- coding: utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
import smtplib

from_addr = 'getvpsresult@163.com' 
password = 'yangmingjia'
smtp_server = 'stmp.163.com'
to_addr = '908210478@qq.com'

def send_email(python_name, result_file):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    # 邮件对象:
    msg = MIMEMultipart()
    msg['From'] = _format_addr('VPS <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header('运行结果', 'utf-8').encode()

    # 邮件正文是MIMEText:
    msg.attach(MIMEText('VPS上\"%s\", 见附件%s' % (python_name, result_file), 'plain', 'utf-8'))

    with open('./nohup.out', 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('text', 'out', filename='nohup.out')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='nohup.out')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server, 587)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

#send_email('sendEmail', 'nohup.out')
