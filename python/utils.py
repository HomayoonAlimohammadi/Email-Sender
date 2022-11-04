from exceptions import SendEmailException

import pandas
import os
import sys
import json
import pandas as pd

from email.mime.application import MIMEApplication
from typing import Any
from html2text import html2text


def get_email_subject_with_interest(base_subject: str, interest: str) -> str:
    return base_subject.format(interest=interest)


def get_email_content(
    email_content_path: str, my_data: Any, prof_data: Any, export: bool = False
) -> str:
    """
    Given the path to the `email_content` template, renders it with the given data and returns the final `string`
    - Parameters:
        - `email_content_path`: path to the email_content template
        - `my_data`: a key-value structure needed to render the template
        - `prof_data`: a key-value structure needed to render the template
        - `export`: if `True`, each email content will be exported with a unique name in ./exported folder
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

    if export:
        file_name = f"{prof_data['university']}_{prof_data['first_name'][0]}_{prof_data['last_name']}.txt"
        export_email_content(email_content=email_content, file_name=file_name)

    return email_content


def export_email_content(email_content: str, file_name: str) -> None:
    """
    Export email content to a .txt file in ./exoprted/
    - Parameters:
        - `email_content`: the actual text file content
        - `file_name`: the name of file
    - Path will be generated if not exists
    """
    current_dir = os.getcwd()
    if not os.path.exists(os.path.join(current_dir, "exported")):
        os.mkdir(os.path.join(current_dir, "exported"))
    path = os.path.join(os.getcwd(), "exported", file_name)
    try:
        with open(path, "w") as f:
            f.write(html2text(email_content))
            print("\033[0;32m exported email content in: \033[0;37m", file_name)
    except Exception as e:
        print(f"\033[1;33m WARNING: unable to export email content: \033[0;37m {path}")


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
            "\033[0;31m error opening email attachment. Check EMAIL_ATTACHMENT_PATH in your .env file \033[0;37m"
        )
        sys.exit(1)
    return attachment


def load_my_data(path: str) -> Any:
    try:
        with open(path, "r") as f:
            my_data = json.load(f)
    except Exception as e:
        print(
            "\033[0;31m error opening my_data json file. Check MY_DATA_PATH in your .env file \033[0;37m"
        )
        sys.exit(1)
    return my_data


def load_all_profs_data(path: str) -> pandas.DataFrame:
    try:
        all_profs_data = pd.read_excel(path)
    except Exception as e:
        print(
            "\033[0;31m error opening all professors data. Check ALL_PROFS_DATA_PATH in your .env file \033[0;37m"
        )
        sys.exit(1)
    return all_profs_data
