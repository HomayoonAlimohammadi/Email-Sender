from exceptions import EmailSenderInitializationException, SendEmailException

import smtplib
import os
import sys
import threading
import pandas

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from dotenv import load_dotenv
from time import time
from typing import Any
from utils import (
    get_email_attachment,
    load_all_profs_data,
    load_my_data,
    get_email_content,
    get_email_subject_with_interest,
)


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
            print("\033[1;32m error setting up the smtp session \033[0;37m")
            raise EmailSenderInitializationException

    def quit_session(self) -> None:
        """
        Makes sure the session is shutdown successfully.
        """
        try:
            self.session.quit()
        except Exception as _:
            ...
        print("\033[1;33m INFO: successfully quit SMTP session. \033[0;37m")

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
        print(f"\033[0;32m Sent mail to {to} \033[0;37m")


def send_email_to_all_profs(
    email_sender: EmailSender,
    base_subject: str,
    email_content_path: str,
    attachment: MIMEApplication,
    my_data: Any,
    all_profs_data: pandas.DataFrame,
    export_all_email_content: bool = False,
    confirm_send: bool = True,
) -> None:
    """
    Handles the whole process of creating an email and exporting the content
    - Parameters:
        - `email_sender`: an instance of EmailSender to handle the SMTP session and mailing process
        - `base_subject`: a template subject which the actual template gets rendered from
        - `email_content_path`: path to the email content template which will get rendered finally
        - `attachment`: an instance of MIMEApplication to attach to the email
        - `my_data`: a key-value structure to render template from
        - `all_profs_data`: a pandas.DataFrame to iterate on and extract individual `profs_data`
        - `export_all_email_content`: if True, every email's content will be exported
        - `'confirm_send`: if False, no email will be actually sent. Works separately with `export_all_email_content`
    """
    threads: list[threading.Thread] = list()
    for _, prof_data in all_profs_data.iterrows():
        email_content = get_email_content(
            email_content_path=email_content_path,
            my_data=my_data,
            prof_data=prof_data,
            export=export_all_email_content,
        )
        subject = get_email_subject_with_interest(base_subject, prof_data["interest"])

        if not confirm_send:
            continue
        try:
            t = threading.Thread(
                target=email_sender.create_and_send_email_message,
                args=(prof_data["email"], subject, email_content, attachment),
            )
            threads.append(t)
            t.start()
        except Exception as e:
            raise SendEmailException

        for t in threads:
            t.join()


def main():

    print("\033[0;36m Made with <3 by Homayoon Alimohammadi \033[0;37m")

    # Start the Timer
    t0 = time()

    load_dotenv()
    MY_DATA_PATH = "../my_data.json"
    EMAIL_CONTENT_PATH = "../email_content.txt"
    ALL_PROFS_DATA_PATH = "../professors.xlsx"
    EMAIL_ATTACHMENT_PATH = "../Resume.pdf"
    SEND_EMAIL = os.environ.get("SEND_EMAIL", "1") == "1"
    EXPORT_CONTENT = os.environ.get("EXPORT_CONTENT", "1") == "1"
    BASE_EMAIL_SUBJECT = (
        "Prospective student interested in {interest} with Machine Learning background"
    )

    my_data = load_my_data(MY_DATA_PATH)
    all_profs_data = load_all_profs_data(ALL_PROFS_DATA_PATH)

    attachment = get_email_attachment(EMAIL_ATTACHMENT_PATH)

    try:
        print("Initializing EmailSender instance...")
        email = my_data.get("email", "")
        password = my_data.get("password", "")
        email_sender = EmailSender(email, password)
        print(
            "\033[1;32m Successfully opened all data files and initialized SMTP session! \033[0;37m"
        )
    except EmailSenderInitializationException as e:
        print("\033[0;31m error initializing the gmail smtp session \033[0;37m")
        sys.exit(1)

    try:
        send_email_to_all_profs(
            email_sender=email_sender,
            base_subject=BASE_EMAIL_SUBJECT,
            email_content_path=EMAIL_CONTENT_PATH,
            attachment=attachment,
            my_data=my_data,
            all_profs_data=all_profs_data,
            export_all_email_content=EXPORT_CONTENT,
            confirm_send=SEND_EMAIL,
        )
    except SendEmailException as e:
        print("\033[0;31m error sending email to professors: \033[0;37m", e)
    finally:
        email_sender.quit_session()

    # Print sending results:
    t1 = time()
    print(f"\033[0;36m Elapsed time: {round(t1 - t0, 2)} seconds. \033[0;37m")


if __name__ == "__main__":
    main()
