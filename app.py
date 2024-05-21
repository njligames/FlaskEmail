from flask import Flask, request, jsonify
from SMTPEmail import SMTPEmail
import os

app = Flask(__name__)

app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
to_email = os.getenv("MAIL_TOEMAIL")

@app.route('/send_mail', methods=['POST'])
def send_mail():
    data = request.json

    subject = data.get('subject')
    html_content = data.get('html_content')

    if not subject or not html_content or not to_email:
        return jsonify({"error": "Missing required fields"}), 400

    sender_email = os.environ["MAIL_USERNAME"]
    password = os.environ["MAIL_PASSWORD"]

    smtpEmail = SMTPEmail()
    smtpEmail.setSubject("loganjamesfolk.com email!")



    wrapper = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
</head>
<body>
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" bgcolor="#f4f4f4">
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="border-collapse: collapse;">
                    <!-- Header -->
                    <tr>
                        <td align="center" bgcolor="#ffffff" style="padding: 40px 0;">
                            <h1 style="color: #333333; font-family: Arial, sans-serif;">{subject}</h1>
                        </td>
                    </tr>
                    <!-- Content -->
                    {html_content}
                    <!-- Footer -->
                    <tr>
                        <td align="center" bgcolor="#f4f4f4" style="padding: 20px 0;">
                            <p style="color: #999999; font-family: Arial, sans-serif; font-size: 12px;">You are receiving this email because you opted in to receive updates from [Your Company/Organization]. To unsubscribe, <a href="[Insert Unsubscribe Link]" style="color: #007bff; text-decoration: underline;">click here</a>.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>

    """











    smtpEmail.setHTMLBody(wrapper)
    smtpEmail.setReceiverEmails([to_email])
    smtpEmail.send(sender_email, password)

    return jsonify({"message": "Email sent successfully"}), 200

if __name__ == '__main__':
    app.run(port=4242)
