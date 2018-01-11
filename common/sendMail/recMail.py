import poplib
import emailAccount
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.utils import parsedate
import time

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

#获取邮件的生成时间 added by mrxu
def get_date(msg):
    if msg != None:
        email_date = parsedate(msg.get('date'))
        return time.strptime('%s-%s-%s' % (email_date[0], email_date[1], email_date[2]), '%Y-%m-%d')
        #return email.utils.parseaddr(msg.get('date'))[1]

# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


email = 'presouce@163.com'
password = emailAccount.password
pop3_server = 'pop.163.com'

def checkMail(sub, days):
    # 连接到POP3服务器:
    server = poplib.POP3(pop3_server)
    # 可以打开或关闭调试信息:
    # server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    # print(server.getwelcome().decode('utf-8'))
    # 身份认证:
    tryFlag = True
    while(tryFlag):
        try:
            server.user(email)
            server.pass_(password)
            tryFlag =False
        except:
            tryFlag = True


    # stat()返回邮件数量和占用空间:
    #print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    #print(mails)

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    flag = False
    for ith in range(index,0, -1):
        resp, lines, octets = server.retr(ith)

        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        subject = decode_str(msg.get('Subject', ''))
        if subject == sub:
            flag =True
            break
        #print(subject)
        #print_info(msg, 0)
        email_date = get_date(msg)
        #print((email_date))
        #print(time.localtime())
        #print(time.mktime(time.localtime()) - time.mktime(email_date)/60/60)    #hr
        if (time.mktime(time.localtime()) - time.mktime(email_date))/60/60/24 > days:
            break

    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)
    # 关闭连接:
    server.quit()
    return flag

#print(checkMail('刀镇星河 第三七八章 无相神斩', 30))

def checkMailList(days):
    # 身份认证:
    tryFlag = True
    while(tryFlag):
        try:
            # 连接到POP3服务器:
            server = poplib.POP3(pop3_server)
            server.user(email)
            server.pass_(password)
            tryFlag =False
        except:
            tryFlag = True


    # stat()返回邮件数量和占用空间:
    #print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    #print(mails)

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    mailList = []
    for ith in range(index,0, -1):
        resp, lines, octets = server.retr(ith)

        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        subject = decode_str(msg.get('Subject', ''))
        mailList.append(subject)

        #print(subject)
        #print_info(msg, 0)
        email_date = get_date(msg)
        #print((email_date))
        #print(time.localtime())
        #print(time.mktime(time.localtime()) - time.mktime(email_date)/60/60)    #hr
        if (time.mktime(time.localtime()) - time.mktime(email_date))/60/60/24 > days:
            break

    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)
    # 关闭连接:
    server.quit()

    return (mailList)
