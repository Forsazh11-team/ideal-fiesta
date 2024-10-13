import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


EMAIL_HOST_PASSWORD = 'etyl yawe aqop ivpo'

def send_emails(sender_email, subject, body, recipient_emails):
    # Настройки SMTP-сервера
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    # Настраиваем соединение с сервером
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Используем шифрование TLS
    server.login(sender_email, EMAIL_HOST_PASSWORD)
    

    with open(body, 'r', encoding='utf-8') as file:
        html_content=file.read()
    # Встраивание трекинг-пикселя
    html_content += f'<img src="http://127.0.0.1:8000/media/trackingpixel.png" alt="" style="display:none;">'

    # Проходим по списку получателей
    for recipient_email in recipient_emails:
        msg = MIMEMultipart()
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Отправляем письмо
        try:
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f'Письмо отправлено на {recipient_email}')
        except Exception as e:
            print(f'Ошибка отправки на {recipient_email}: {str(e)}')
    
    # Закрываем соединение с сервером
    server.quit()

if __name__ == "__main__":
    sender_email = 'trappedinthetrench@gmail.com'  # Ваш email
    subject = 'Ваш аккаунт под угрозой!'
    body = 'phishing.html'

    # Список получателей
    recipient_emails = ['dkflf1002@yandex.ru']

    send_emails(sender_email, subject, body, recipient_emails)