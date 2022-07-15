import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import json
from typing import Any, Dict
import pandas as pd
import pandas


class EmailSender:
    def __init__(
        self,
        my_data_path: str,
        profs_data_path: str,
        resume_path: str,
        content_path: str,
    ):
        self.my_data_path = my_data_path
        self.profs_data_path = profs_data_path
        self.resume_path = resume_path
        self.content_path = content_path
        self.cache: Dict[str, Any] = {}
        self.load_my_data()
        self.load_profs_data()
        self.login_to_email()

    def load_my_data(self) -> None:
        with open(self.my_data_path, "r") as f:
            self.my_data = json.load(f)
        self.email: str = self.my_data["email"]

    def load_profs_data(self) -> None:
        with open(self.profs_data_path, "r") as f:
            self.profs_data: pd.DataFrame = pd.read_excel("professors.xlsx")

    def login_to_email(self) -> None:
        email = self.my_data["email"]
        password = self.my_data["password"]
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.ehlo()
        session.starttls()
        session.login(email, password)
        self.session: smtplib.SMTP = session

    def configure_email_message(self, prof_data) -> MIMEMultipart:
        subject = self.my_data["subject"]
        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = prof_data["email"]
        message["Subject"] = subject
        mail_content = self.get_mail_content(prof_data)
        message.attach(MIMEText(mail_content, "html"))

        with open(self.resume_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")

        attach.add_header("Content-Disposition", "attachment", filename="Resume.pdf")
        message.attach(attach)
        return message

    def get_mail_content(self, prof_data) -> str:
        with open(self.content_path, "r") as f:
            raw_content = f.read()
        mail_content = raw_content.format(
            last_name=prof_data["last_name"],
            university=prof_data["university"],
            field=prof_data["field"],
            my_field=self.my_data["field"],
            my_university=self.my_data["university"],
            my_country=self.my_data["country"],
            gpa=self.my_data["gpa"],
            toefl_score=self.my_data["toefl_score"],
            gre_score=self.my_data["gre_score"],
            paper=prof_data["paper"],
            my_goal=self.my_data["my_goal"],
            my_first_name=self.my_data["first_name"],
        )
        return mail_content

    def send_email(self, prof_data: pandas.Series) -> None:
        message = self.configure_email_message(prof_data)
        text = message.as_string()
        self.session.sendmail(self.email, prof_data["email"], text)

    def send_email_to_all_profs(self) -> None:
        for idx, prof_data in self.profs_data.iterrows():
            self.send_email(prof_data=prof_data)
            print(f"{idx+1} - Mail Sent to {prof_data['email']}")
        self.session.quit()


def main():

    # Replace with real data files.
    my_data_path = "./my_data_fake.json"
    profs_data_path = "./professors.xlsx"
    content_path = "./email_content.txt"
    resume_path = "./Resume.pdf"
    email_sender = EmailSender(
        my_data_path=my_data_path,
        profs_data_path=profs_data_path,
        content_path=content_path,
        resume_path=resume_path,
    )
    email_sender.send_email_to_all_profs()


if __name__ == "__main__":
    main()
