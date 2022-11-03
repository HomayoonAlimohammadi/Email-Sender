from exceptions import EmailSenderInitializationException, SendEmailException

import smtplib
import pandas
import os
import sys
import json
import pandas as pd

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from typing import Any
from dotenv import load_dotenv


class EmailSender:
    """
    EmailSender can be utilized to initialize an SMTP session given correct credentials.
    This service then will be able to send emails given sufficient inputs.
    - Parameters:
        - `email`: indicating your email (FROM)
        - `password`: your email password, WARNING: this"""

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        try:
            self.setup_smpt_session()
        except Exception as e:
            self.quit_session()
            print("error setting up the smtp session")
            raise EmailSenderInitializationException

    def quit_session(self) -> None:
        try:
            self.session.quit()
        except Exception as _:
            ...
        print("\033[1;33m INFO: successfully quit SMTP session.")

    def setup_smpt_session(self) -> None:
        """
        Setup SMPT gmail session given the email and app password
        """
        self.session = smtplib.SMTP("smtp.gmail.com", 587)
        self.session.ehlo()
        self.session.starttls()
        self.session.login(self.email, self.password)

    def create_and_send_email_message(
        self,
        to: str,
        subject: str,
        email_content: str,
        attachment: MIMEApplication | None,
    ) -> None:
        """
        `Create` a MIMEMultipart `Message` and then `send` it using the initialized `session`.
        - Parameters:
            - `to`: indicating the recipient
            - `subject`: containing the email subject
            - `email_content`: to include as the email main body
            - `attachment`: an optional file to be attached to the email message
        """
        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(email_content, "html"))
        if attachment:
            message.attach(attachment)
        self.session.sendmail(self.email, to, message.as_string())
        print(f"\033[0;32m Sent mail to {to}")


def get_email_subject_with_interest(base_subject: str, interest: str) -> str:
    return base_subject.format(interest=interest)


def get_email_content(email_content_path: str, my_data: Any, prof_data: Any) -> str:
    """
    Given the path to the `email_content` template, renders it with the given data and returns the final `string`
    - Parameters:
        - `email_content_path`: path to the email_content template
        - `prof_data`: a key-value structure needed to render the template
    """
    with open(email_content_path, "r") as f:
        raw_content = f.read()
    email_content = raw_content.format(
        my_first_name=my_data["first_name"],
        my_last_name=my_data["last_name"],
        my_major=my_data["major"],
        my_university=my_data["university"],
        my_city=my_data["city"],
        my_country=my_data["country"],
        my_gpa=my_data["gpa"],
        my_toefl=my_data["toefl"],
        my_website=my_data["website"],
        prof_last_name=prof_data["last_name"],
        prof_interest=prof_data["interest"],
        prof_first_paper=prof_data["first_paper"],
        prof_first_paper_year=prof_data["first_paper_year"],
        prof_second_paper=prof_data["second_paper"],
        prof_second_paper_year=prof_data["second_paper_year"],
        target_degree=prof_data["target_degree"],
        prof_university=prof_data["university"],
    )
    return email_content


def get_email_attachment(path: str, file_name: str = "") -> MIMEApplication:
    """
    Given the path to the attachment file and an optional file_name, returns a `MIMEApplication` object
    - Parameters:
        - `path`: a string indicating the path to the actual file
        - `file_name`: an optional string. If not provided, will be extracted from the path
    """
    if "." in path:
        subtype = path.split(".")[-1]
    else:
        subtype = ""
    try:
        with open(path, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype=subtype)

        if not file_name:
            if "." in path:
                file_name = path.split(".")[-2] + "." + path.split(".")[-1]
            else:
                file_name = path
        attachment.add_header("Content-Disposition", "attachment", filename=file_name)
    except Exception as e:
        print(
            "\033[0;31m error opening email attachment. Check EMAIL_ATTACHMENT_PATH in your .env file"
        )
        sys.exit(1)
    return attachment


def load_my_data(path: str) -> Any:
    try:
        with open(path, "r") as f:
            my_data = json.load(f)
    except Exception as e:
        print(
            "\033[0;31m error opening my_data json file. Check MY_DATA_PATH in your .env file"
        )
        sys.exit(1)
    return my_data


def load_all_profs_data(path: str) -> pandas.DataFrame:
    try:
        all_profs_data = pd.read_excel(path)
    except Exception as e:
        print(
            "\033[0;31m error opening all professors data. Check ALL_PROFS_DATA_PATH in your .env file"
        )
        sys.exit(1)
    return all_profs_data


def send_email_to_all_profs(
    email_sender: EmailSender,
    base_subject: str,
    email_content_path: str,
    attachment: MIMEApplication,
    my_data: Any,
    all_profs_data: pandas.DataFrame,
) -> None:
    for _, prof_data in all_profs_data.iterrows():
        email_content = get_email_content(email_content_path, my_data, prof_data)
        subject = get_email_subject_with_interest(base_subject, prof_data["interest"])
        try:
            email_sender.create_and_send_email_message(
                to=prof_data["email"],
                subject=subject,
                email_content=email_content,
                attachment=attachment,
            )
        except Exception as e:
            raise SendEmailException


def main():

    load_dotenv()
    MY_DATA_PATH = os.environ.get("MY_DATA_PATH", "")
    EMAIL_CONTENT_PATH = os.environ.get("EMAIL_CONTENT_PATH", "")
    ALL_PROFS_DATA_PATH = os.environ.get("ALL_PROFS_DATA_PATH", "")
    EMAIL_ATTACHMENT_PATH = os.environ.get("EMAIL_ATTACHMENT_PATH", "")
    BASE_EMAIL_SUBJECT = (
        "Prospective student interested in {interest} with Machine Learning background"
    )
    print(MY_DATA_PATH, ALL_PROFS_DATA_PATH, EMAIL_ATTACHMENT_PATH, EMAIL_CONTENT_PATH)

    my_data = load_my_data(MY_DATA_PATH)
    all_profs_data = load_all_profs_data(ALL_PROFS_DATA_PATH)

    attachment = get_email_attachment(EMAIL_ATTACHMENT_PATH)

    try:
        print("Initializing EmailSender instance...")
        email = my_data.get("email", "")
        password = my_data.get("password", "")
        email_sender = EmailSender(email, password)
        print(
            "\033[1;32m Successfully opened all data files and initialized SMTP session!"
        )
    except EmailSenderInitializationException as e:
        print("\033[0;31m error initializing the gmail smtp session")
        sys.exit(1)

    try:
        send_email_to_all_profs(
            email_sender=email_sender,
            base_subject=BASE_EMAIL_SUBJECT,
            email_content_path=EMAIL_CONTENT_PATH,
            attachment=attachment,
            my_data=my_data,
            all_profs_data=all_profs_data,
        )
    except SendEmailException as e:
        print("\033[0;31m error sending email to professors\n", e)
    finally:
        email_sender.quit_session()


if __name__ == "__main__":
    main()
