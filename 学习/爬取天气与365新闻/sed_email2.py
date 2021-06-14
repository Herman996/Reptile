import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# HOST = 'smtp.163.com'
# 设置邮件标题
# SUBJECT = '每日简报'
# 设置发件人的邮箱
# FROM = 'tjf19968743@163.com'
# PWD = "ESEBPZBFCDHUOVZU"
PORT = 465

HOST = "smtp.qq.com"
FROM = "2360316087@qq.com"
PWD = "yvfnsmkmjexqechf"
# 设置收件人的邮箱，可以一次性发送给多个人，这里我把邮件自己发给自己
# TO = '951803764@qq.com'
# TO = ['tjf19968743@163.com','951803764@qq.com','hermantang@easyops.cn']
# TO = ['hermantang@easyops.cn']
# 表示使用内嵌资源的形式，将邮件发送给对方，这里的内容是空的，相当于一个空的信封。
def sed_email(info, TO, SUBJECT):
    for to_user in TO:
        message = MIMEMultipart('related')
        # --------------------发送文本内容 - --------------------------
        # 编写邮件的内容，必须为字符串，plain为内容的类型格式，文本类型默认为plain，编码格式为utf-8，相当于一张信
        message_html = MIMEText(info, 'plain', 'utf-8')
        # 将邮件的内容放到邮件信息中去，就像我们把信装进信封
        message.attach(message_html)
        # ---------------------发送一个图片 - --------------------------
        # 读取这个文件，然后设置格式为base64。
        # message_image = MIMEText(open('../images.jpg', 'rb').read(), 'base64', 'utf-8')
        # # 设置这个图片为邮件的附件，并且设置名字。
        # message_image['Content-disposition'] = 'attachment;filename="wait.jpg"'
        # # 将图片放入到邮件信息中去。
        # message.attach(message_image)
        # ----------------------发送一个表格附件 - ----------------------
        # 与发送图片时格式相同
        # message_xlsx = MIMEText(open('people.xlsx', 'rb').read(), 'base64', 'utf-8')
        # message_xlsx['Content-Disposition'] = 'attachment;filename="test1111.xlsx"'
        # message.attach(message_xlsx)
        email_client = smtplib.SMTP_SSL(host=HOST)
        # 设置发件人邮箱的域名端口，端口为465
        email_client.connect(host=HOST, port=PORT)
        # 密码千万不要写邮箱密码，要写邮箱的授权码
        result = email_client.login(FROM, PWD)
        print('登录结果', result)

    # 设置收件人
        message['To'] = to_user
        message['From'] = FROM  # 设置收件人
        # 发送的邮件
        message['Subject'] = SUBJECT
        # 获取简单邮件传输协议证书
        # 发送邮件，msg后面的结果必须是一个字符串，as_string将整个对象转成字符串
        email_client.sendmail(from_addr=FROM, to_addrs=to_user, msg=message.as_string())
    # 关闭邮件发送客户端
        email_client.close()

if __name__ == '__main__':
    TO = ['hermantang@easyops.cn'] 
    SUBJECT = '每日简报'
    sed_email('本周周末公司在XXX酒店三楼306房间进行聚会，特邀您参加!!!', TO, SUBJECT)
