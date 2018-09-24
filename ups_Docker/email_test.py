import smtplib

if __name__ == "__main__":
    host = "smtp.gmail.com"
    port = 465
    user = "youlyu25@gmail.com"
    pwd = "abc12345678!"
    s = smtplib.SMTP_SSL(host, port)
    s.login(user, pwd)
    receiver = "youlyu@outlook.com"
    s.sendmail(user, receiver, "hello, berlinix!")
