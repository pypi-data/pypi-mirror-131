import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import List


class EmailSendService:
    def __init__(
        self,
        receivers_accounts: List[str],
        sender_account: str,
        sender_password: str,
        smtp_host: str,
        smtp_port: int,
    ):
        self.receivers_accounts = receivers_accounts
        self.sender_account = sender_account
        self.sender_password = sender_password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)

    def send_attachments(
        self,
        file_path_list: List[str],
        subject: str,
        text: str,
        head_to: str = "dear",
        head_from: str = "蜗牛保险",
    ):
        """
        :param file_path_list: 要发送的附件列表
        :param subject: 邮件主题
        :param text: 邮件正文
        :param head_to: 头部接受者昵称
        :param head_from: 头部发送者昵称
        :return:
        """
        # 创建一个带附件的实例
        message = MIMEMultipart()
        # message['From'] = Header(head_from, 'utf-8')
        message["From"] = formataddr((head_from, self.sender_account), "utf-8")
        # message['To'] = Header(head_to, 'utf-8')
        message["To"] = formataddr(
            (head_to, ",".join(self.receivers_accounts)), "utf-8"
        )
        message["Subject"] = Header(subject, "utf-8")

        # 邮件正文内容
        message.attach(MIMEText(text, "plain", "utf-8"))

        # 添加附件
        for file_path in file_path_list:
            # 构造附件
            att = MIMEText(open(file_path, "rb").read(), "base64", "utf-8")
            att["Content-Type"] = "application/octet-stream"
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            file_name = file_path.split("/")[-1]
            att["Content-Disposition"] = f'attachment; filename="{file_name}"'
            message.attach(att)
        else:
            pass

        try:
            # self.server.connect(config.SMTP_HOST)
            self.server.login(self.sender_account, self.sender_password)
            self.server.sendmail(
                self.sender_account, self.receivers_accounts, message.as_string()
            )
            self.server.quit()
            print(f"邮件发送成功: {'，'.join(file_path_list)}")
        except Exception as e:
            print(f"邮件发送失败, error: {str(e)}; {'，'.join(file_path_list)}")
