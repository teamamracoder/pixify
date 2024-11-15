class EmailTemplate:
    def __init__(self, subject: str, message: str) -> None:
        self.__subject = subject
        self.__message = message

    def get_subject(self, **kwargs) -> str:
        subject = self.__subject
        for key, value in kwargs.items():
            subject = subject.replace(f"{{{key}}}", str(value))
        return subject

    def get_message(self, **kwargs) -> str:
        message = self.__message
        for key, value in kwargs.items():
            message = message.replace(f"{{{key}}}", str(value))
        return message


welcome_template = EmailTemplate(
    subject="Welcome to Pixify",
    message="""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to Pixify!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                    <img src="https://st3.depositphotos.com/43745012/44906/i/450/depositphotos_449066958-stock-photo-financial-accounting-logo-financial-logo.jpg" alt="..." width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <p>Hi {first_name},</p>
                    <p>Welcome to Pixify! 🎉</p>
                    <p>You're now part of our community! Get ready to dive into a world of Pixify.</p>

                    <p>For any questions, simply click below:</p>
                    <p>Happy browsing!</p>
                    <p>Best Regards,<br>{full_name}<br>Pixify</p>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Pixify | Privacy Policy | Support</p>
                        <p>© 2024 Pixify. All Rights Reserved.</p>
                    </footer>
                </div>

                </body>
                </html>
            """,
)

otp_template = EmailTemplate(
    subject="OTP to Login",
    message="""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to Pixify!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                        <img src="https://st3.depositphotos.com/43745012/44906/i/450/depositphotos_449066958-stock-photo-financial-accounting-logo-financial-logo.jpg" alt="..." width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <main class="content" style="text-align: start; margin-bottom: 20px;">
                        <p>Hi,</p>
                        <p>Welcome to Pixify! For security purposes, please enter the OTP code provided below to verify your email.</p>
                        <h3>{otp}</h3>
                        <p>OTP is confidential and is valid for 5 minutes.</p>
                        <p>Best Regards,</p>
                        <p>Pixify Team</p>
                    </main>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Pixify | Privacy Policy | Support</p>
                        <p>© 2024 Pixify. All Rights Reserved.</p>
                    </footer>
                </div>

                </body>
                </html>
            """,
)
