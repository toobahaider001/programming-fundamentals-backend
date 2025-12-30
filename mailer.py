import os
import resend
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL") 

resend.api_key = RESEND_API_KEY

def format_submission_email(content: dict) -> str:
    lines = []

    lines.append(f"<h2>Project Evaluation Result</h2>")
    lines.append(f"<p><strong>Project Title:</strong> {content['project_details']['title']}</p>")
    lines.append(f"<p><strong>Description:</strong> {content['project_details']['description']}</p>")
    lines.append(
        f"<p><strong>Code File:</strong> "
        f"<a href='{content['project_details']['code_file_path']}'>Google Drive Link</a></p>"
    )
    lines.append(f"<p><strong>Marks:</strong> {content['marks']}</p>")
    lines.append(f"<p><strong>Status:</strong> {content['status']}</p>")
    lines.append("<h3>Students</h3><ul>")

    for member in content.get("members", []):
        lines.append(
            f"<li>{member['student_name']} ({member['student_id']})</li>"
        )

    lines.append("</ul>")

    return "\n".join(lines)


def send_email_message(to_email: str, subject: str, content: dict):
    try:
        html_body = format_submission_email(content)

        params: resend.Emails.SendParams = {
            "from": FROM_EMAIL,
            "to": [to_email],
            "subject": subject,
            "html": html_body,
        }

        resend.Emails.send(params)

    except Exception as e:
        print("Email failed:", e)