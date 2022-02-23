import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import pandas as pd
from numpy import var


def send_mail(variables, mail_content, receiver_address):
    sender_address = variables['sender_address']
    sender_pass = variables['sender_pass']
    subject = variables['subject']
    #The mail addresses and password
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))
    
    with open('./Resume.pdf', "rb") as f:
        #attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
        attach = MIMEApplication(f.read(),_subtype="pdf")
    attach.add_header('Content-Disposition','attachment',filename='Resume.pdf')
    message.attach(attach)
        
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print(f'Mail Sent to {receiver_address}')


def content_maker(variables, prof_data):
    my_firstname = variables['my_firstname']
    my_university_name = variables['my_university_name']
    my_field = variables['my_field']
    paper_title = variables['paper_title']
    nth_author = variables['nth_author']
    gpa = variables['gpa']
    toefl_score = variables['toefl_score']
    gre_score = variables['gre_score']
    my_goal = variables['my_goal']
    my_country = variables['my_country']

    # Professor's Data
    firstname = prof_data['firstname']
    lastname = prof_data['lastname']
    target_university_name = prof_data['target_university_name']
    her_field = prof_data['her_field']
    her_article = prof_data['her_article']



    mail_content = f'''Dear Prof. Dr. {firstname[0].upper()}. {lastname},<br><br>
    
    I turn to you for the <b>Master position</b> on {target_university_name} in the area of {her_field}. I hold a <b>BSc. in {my_field}</b> from the <b>best university of the country</b>, <b>{my_university_name}, {my_country}</b>. My journal paper <b>{paper_title}</b> as a <b>{nth_author}</b> was recently published as well. 
    <br><br>
    I have a <b>GPA</b> of <b>{gpa}</b>, and also I have already passed <b>TOEFL</b> with a total score of <b>{toefl_score}</b>, paired with a <b>{gre_score} in GRE</b>. 
    <br><br>
    I have reviewed your faculty profile and am interested in the work that you have done. I was intrigued by your journal article, <b>{her_article}</b>. I would like to get involved in research in this area because it will help me to better prepare for my feature as a <b>{my_goal}</b>.
    <br><br>
    Kindly find the attached <b>CV</b>, and would love to provide you with further documents if needed.  If the process will be manageable, I would look forward to being a part of your research.
    <br><br>
    I will wait for your kind response.<br>
    Sincerely yours,<br>
    {my_firstname}.
    '''
    return mail_content
    



with open('./variables.json', 'r') as f:
    variables = json.load(f)


profs = pd.read_excel('professors.xlsx')
for row in range(len(profs)):
    prof_data = profs.iloc[row,:].to_dict()
    receiver_address = prof_data['receiver_address']
    mail_content = content_maker(variables=variables, prof_data=prof_data)
    send_mail(variables=variables, mail_content=mail_content, receiver_address=receiver_address)
