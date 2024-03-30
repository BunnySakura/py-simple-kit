import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from typing import List


class MailSender:
    """更健壮、更易用、功能更丰富的邮件发送类。

    Attributes:
        mail_host: 邮箱服务器地址。
        mail_pwd: 发件人邮箱的授权码。
        sender: 发件人的邮箱地址。
        receivers: 收件人的邮箱地址列表。
    """

    def __init__(self, mail_host: str, mail_pwd: str, sender: str, receivers: List[str]):
        """初始化邮件服务。

        Args:
            mail_host: 邮箱服务器地址。
            mail_pwd: 发件人邮箱的授权码。
            sender: 发件人的邮箱地址。
            receivers: 收件人的邮箱地址列表。
        """
        self.mail_host = mail_host
        self.mail_pwd = mail_pwd
        self.sender = sender
        self.receivers = receivers

    def send_email(self, subject: str, message: str, attachments: List[str] = None, is_html: bool = False):
        """发送邮件。

        Args:
            subject: 邮件主题。
            message: 邮件正文内容。
            attachments: 附件文件路径列表。

        Returns:
            无。
        """
        if attachments is None:
            attachments = []
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = ", ".join(self.receivers)
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'html' if is_html else 'plain', 'utf-8'))

            for index, attachment in enumerate(attachments):
                with open(attachment, 'rb') as file:
                    file_data = file.read()
                if self.is_image(attachment):
                    msg.attach(MIMEText(f'<img src="cid:image{index}">', "html", 'utf-8'))
                    part = MIMEImage(file_data, Name=attachment)
                    part.add_header("Content-ID", f"<image{index}>")
                else:
                    part = MIMEApplication(file_data, Name=attachment)
                    part.add_header("Content-Disposition", "attachment", filename=attachment)
                msg.attach(part)

            with smtplib.SMTP_SSL(self.mail_host, 465) as server:
                server.login(self.sender, self.mail_pwd)
                server.sendmail(self.sender, self.receivers, msg.as_string())

            print('邮件发送成功')
        except smtplib.SMTPException as smtp_error:
            print('邮件发送失败', smtp_error)

    @staticmethod
    def is_image(img_path: str) -> bool:
        """
        通过后缀名判断文件是否是图片
        Args:
            img_path: 文件路径

        Returns:
            true表示图片，false则不是
        """
        image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        extension = img_path.split('.')[-1].lower()
        return extension in image_extensions


# 使用示例
if __name__ == "__main__":
    mail_host = "smtp.qq.com"
    mail_pwd = "your_mail_password"
    sender = "your_email@example.com"
    receivers = ["recipient1@example.com", "recipient2@example.com"]

    mailer = MailSender(mail_host, mail_pwd, sender, receivers)

    email_subject = "邮件主题"
    email_text = "邮件正文内容"
    attachments = ["attachment1.txt", "attachment2.pdf"]

    mailer.send_email(email_subject, email_text, attachments, is_html=True)
