from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
to_email = os.getenv("MAIL_TOEMAIL")

mail = Mail(app)

@app.route('/send_mail', methods=['POST'])
def send_mail():
    data = request.json

    from_email = data.get('from_email')
    subject = data.get('subject')
    html_content = data.get('html_content')

    if not from_email or not subject or not html_content or not to_email:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        msg = Message(
            subject=subject,
            sender=from_email,
            recipients=[to_email],
            html=html_content
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=4242)
