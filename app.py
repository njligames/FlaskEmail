from SMTPEmail import SMTPEmail
import os

app = Flask(__name__)

# Configure Flask-Mail
# app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
# app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
to_email = os.getenv("MAIL_TOEMAIL")

mail = Mail(app)

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
    smtpEmail.setSubject(subject)
    smtpEmail.setHTMLBody(html_content)
    smtpEmail.setReceiverEmails([to_email])
    smtpEmail.send(sender_email, password)

if __name__ == '__main__':
    app.run(port=4242)
