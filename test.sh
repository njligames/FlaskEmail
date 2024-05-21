curl -X POST https://flaskemail.onrender.com/send_mail \
    -H "Content-Type: application/json" \
    -d '{
        "from_email": "your_email@example.com",
        "to_email": "recipient_email@example.com",
        "subject": "Test Subject",
        "html_content": "<h1>Hello, World!</h1>"
    }'
