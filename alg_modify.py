import os
import time
import smtplib
from email.mime.text import MIMEText
# 设置文件路径和时间阈值（12.5分钟）
file_path = "/home/sportvision/highlight_code/alg_time.txt"
time_threshold = 700 # 单位为秒

# 获取文件的修改时间和当前时间，并计算它们之间的时间差
file_mod_time = os.path.getmtime(file_path)
current_time = time.time()
time_diff = current_time - file_mod_time

# 判断时间差是否小于时间阈值，如果是则打印信息，否则运行 Bash 脚本
if time_diff < time_threshold:
    print("File modified in the last 10 minutes.")
else:
    # 设置邮件内容
    mail_content = "The file {} has not been modified in the last 10 minutes.".format(file_path)
    mail_subject = "Alert: File not modified"

    # 发件人、收件人和邮件服务器配置
    from_address = "13066905418@163.com"
    to_address = "1257776077@qq.com"
    smtp_server = "smtp.163.com"
    # smtp_port = 587
    smtp_user = "13066905418@163.com"
    smtp_password = "OAYXRINPPKAIFSDI"

    # 创建邮件对象
    mail = MIMEText(mail_content)
    mail["Subject"] = mail_subject
    mail["From"] = from_address
    mail["To"] = to_address

    # 发送邮件
    try:
        smtp = smtplib.SMTP(smtp_server)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.sendmail(from_address, to_address, mail.as_string())
        smtp.quit()
        print("Mail sent successfully.")
    except Exception as e:
        print("Error sending mail:", e)

    # 运行 Bash 脚本
    # os.system("bash /home/sportvision/highlight_code/main.sh")
