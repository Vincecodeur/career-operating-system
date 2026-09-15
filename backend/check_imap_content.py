import imaplib

from app.core.database import SessionLocal
from app.auth.models import User
from app.jobs.connectors.credentials_resolver import (
    resolve_linkedin_email_credentials,
)


def run_check():
    db = SessionLocal()
    user = db.query(User).filter(
        User.email == "maw282003@gmail.com"
    ).first()

    credentials = resolve_linkedin_email_credentials(db, user.id)

    connection = imaplib.IMAP4_SSL(
        credentials["imap_host"],
        credentials["imap_port"],
    )
    connection.login(
        credentials["email_address"],
        credentials["app_password"],
    )
    connection.select(credentials["folder"])

    status, data = connection.search(None, "ALL")
    all_ids = data[0].split()
    folder_name = credentials["folder"]
    print("Total emails dans", folder_name, ":", len(all_ids))

    status, data = connection.search(None, "UNSEEN")
    unseen_ids = data[0].split()
    print("Emails non lus:", len(unseen_ids))

    if all_ids:
        last_id = all_ids[-1]
        status, msg_data = connection.fetch(
            last_id,
            "(BODY[HEADER.FIELDS (FROM SUBJECT)])",
        )
        print("Dernier email recu:")
        print(msg_data[0][1].decode(errors="replace"))

    connection.close()
    connection.logout()
    db.close()


if __name__ == "__main__":
    run_check()
