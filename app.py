from flask import Flask, request, jsonify
from SMTPEmail import SMTPEmail
import os

app = Flask(__name__)

app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
to_email = os.getenv("MAIL_TOEMAIL")

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Send Email</title>
    </head>
    <body>
        <h1>Send Email</h1>
        <form id="emailForm">
            <label for="from_email">From Email:</label><br>
            <input type="email" id="from_email" name="from_email" required><br><br>

            <label for="to_email">To Email:</label><br>
            <input type="email" id="to_email" name="to_email" required><br><br>

            <label for="subject">Subject:</label><br>
            <input type="text" id="subject" name="subject" required><br><br>

            <label for="html_content">HTML Content:</label><br>
            <textarea id="html_content" name="html_content" required></textarea><br><br>

            <button type="submit">Send Email</button>
        </form>

        <script>
            document.getElementById('emailForm').addEventListener('submit', function(event) {
                event.preventDefault();

                const fromEmail = document.getElementById('from_email').value;
                const toEmail = document.getElementById('to_email').value;
                const subject = document.getElementById('subject').value;
                const htmlContent = document.getElementById('html_content').value;

                const data = {
                    from_email: fromEmail,
                    to_email: toEmail,
                    subject: subject,
                    html_content: htmlContent
                };

                fetch('/send_mail', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert('Error: ' + data.error);
                    } else {
                        alert('Email sent successfully');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error: ' + error);
                });
            });
        </script>
    </body>
    </html>
    '''

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
