import imaplib
import email
from email.header import decode_header
import re
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER, IMAP_PORT, KEYWORDS, REJECT_URLS
from email_summarizer import summarize_email

def connect_to_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select('inbox') 
    return mail

def search_emails(mail):
    type, data = mail.search(None, 'UNSEEN')  # Only searching for unread emails
    mail_ids = data[0]
    id_list = mail_ids.split()
    summarized_emails = []

    for num in id_list[::-1]:  # The function will start reading from the latest email
        typ, data = mail.fetch(num, '(RFC822)') 
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = decode_header(msg['subject'])[0][0]
                if isinstance(email_subject, bytes):
                    email_subject = email_subject.decode()
                email_body = get_email_body(msg)
                if any(keyword.lower() in email_body.lower() for keyword in KEYWORDS):
                    if not any(reject_url in email_body for reject_url in REJECT_URLS):
                        summary = summarize_email(email_body)
                        summarized_emails.append((email_subject, summary))
    return summarized_emails

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = part.get("Content-Disposition")
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()  # Get the plain text emails
    else:
        return msg.get_payload(decode=True).decode()

if __name__ == "__main__":
    mail = connect_to_email()
    emails = search_emails(mail)
    for subject, summary in emails:
        print(f"Subject: {subject}\nSummary: {summary}\n")
