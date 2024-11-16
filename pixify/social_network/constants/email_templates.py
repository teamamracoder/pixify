class DefaultTemplate:
    def _init_(self, data: dict) -> None:
        self.data = data

    def get_key(self, val: str) -> str:
        for key, value in self.data.items():
            if value == val:
                return key

    def get_value(self, key: str) -> str:
        return self.data.get(key)


email_templates = DefaultTemplate(
    {
        "WELCOME_TEMPLATE": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Thank You for Signup In!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                    <img src="https://st3.depositphotos.com/43745012/44906/i/450/depositphotos_449066958-stock-photo-financial-accounting-logo-financial-logo.jpg" alt="Sagar-Services Logo" width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <p>Hi [FIRST_NAME],</p>
                    <p>Welcome to Sagar Electronics! 🎉</p>
                    <p>You're now part of our community! Get ready to dive into a world of electronic wonders, from CPUs and laptops to desktops, motherboards, keyboards, mouse, and more.</p>
                    <p>Here's what you get:</p>
                    <ol>
                        <li>Top-quality electronics at great prices</li>
                        <li> Fast shipping</li>
                        <li>Awesome customer support</li>
                    </ol>

                    <p>For any questions, simply click below:</p>
                    <p>Happy browsing!</p>
                    <p>Best Regards,<br>[FULL_NAME]<br>Sagar Electronics</p>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Sagar-Services | Privacy Policy | Support</p>
                        <p>© 2024 Sagar-Services. All Rights Reserved.</p>
                    </footer>
                </div>

                </body>
                </html>
            """,
        "OTP_TEMPLATE": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to Sagar-Services!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                        <img src="companyLogo.png" alt="Sagar-Services Logo" width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <main class="content" style="text-align: start; margin-bottom: 20px;">
                        <p>Hi [FIRST_NAME],</p>
                        <p>Welcome to Sagar-Services! For security purposes, please enter the OTP code provided below to verify your email.</p>
                        <h3>[OTP]</h3>
                        <p>OTP is confidential and is valid for 3 minutes.</p>
                        <p>Best Regards,</p>
                        <p>The Sagar-Services Team</p>
                    </main>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Sagar-Services | Privacy Policy | Support</p>
                        <p>© 2024 Sagar-Services. All Rights Reserved.</p>
                    </footer>
                </div>

                </body>
                </html>
            """,
        "ORDER_STATUS_TEMPLATE": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Order Status Update</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); ">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                        <img src="companyLogo.png" alt="Sagar-Services Logo" width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <main class="content" style="text-align: start; margin-bottom: 20px;">
                        <p>Hi Arif,</p>
                        <p>We're reaching out to provide you with an update on your recent order with us. Your order number is: <b>[ORDER_NUMBER]</b>.</p>
                        <p>We're pleased to inform you that your order is <b>[ORDER_STATUS]</b>. You can track the progress of your order by clicking the button below:</p>
                        <p>If you have any questions or concerns regarding your order, please don't hesitate to contact our customer support team at <a href="tel:" style="color:black;text-decoration: none;">9775116594</a> | <a href="mailto:team.amracode@gmail.com" style="color:black;text-decoration: none;">team.amracode@gmail.com</a>.com. We're here to assist you every step of the way.</p>
                        <p>Thank you for choosing us for your purchase. We appreciate your business and look forward to serving you again in the future.</p>
                        <p>Best regards,</p>
                        <p>The Sagar-Services Team</p>
                    </main>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Sagar-Services | Privacy Policy | Support</p>
                        <p>© 2024 Sagar-Services. All Rights Reserved.</p>
                    </footer>
                </div>
                </body>
                </html>
            """,
        "STAFF_ROLE_ADD_TEMPLATE": """
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to Sagar-Services!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                        <img src="companyLogo.png" alt="Sagar-Services Logo" width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <main class="content" style="text-align: start; margin-bottom: 20px;">
                        <p>Hi [FULL_NAME],</p>
                        <p>I'm excited to congratulate you on becoming a part of our <b>staff!</b> Your hard work and skills have earned you this well-deserved promotion.</p>
                        <p>Your positive attitude and dedication make you a perfect fit for this role. I have no doubt you'll thrive in it and make a real difference to our team.</p>
                        <p>If you need any help settling in, just let me know. We're here to support you all the way.</p>
                        <p>Best Regards,</p>
                        <p>The Sagar-Services Team</p>
                    </main>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Sagar-Services | Privacy Policy | Support</p>
                        <p>© 2024 Sagar-Services. All Rights Reserved.</p>
                    </footer>
                </div>
                </body>
                </html>
            """,
        "THANK_YOU_TEMPLATE": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to Sagar-Services!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); ">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                        <img src="companyLogo.png" alt="Sagar-Services Logo" width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <main class="content" style="text-align: start; margin-bottom: 20px;">
                        <h1>Thank You for Shopping with Sagar-co!</h1>
                        <p>Hi [FULL_NAME],</p>
                        <p>We appreciate your recent purchase and hope you had an exceptional shopping experience. Your feedback is important to us and helps us improve our services.</p>
                        <p>We kindly ask you to take a moment to share your thoughts on your recent shopping experience. Your input means a lot to us!</p>
                        <p>Thank you for your support!</p>
                        <p>Best wishes,</p>
                        <p>The Sagar-co Team</p>
                    </main>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Sagar-Services | Privacy Policy | Support</p>
                        <p>© 2024 Sagar-Services. All Rights Reserved.</p>
                    </footer>
                </div>
                </body>
                </html>
            """,
        "SENT_COUPON_TEMPLATE": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to Sagar-Services!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); ">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                        <img src="companyLogo.png" alt="Sagar-Services Logo" width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <main class="content" style="text-align: start; margin-bottom: 20px;">
                        <h1>Thank You for Shopping with Sagar-co!</h1>
                        <p>Hi [FULL_NAME],</p>
                        <p> Congratulations..! your a lucky customer for Sagar-co!</p>
                        <p> You Got a coupon code -  [COUPON_CODE] <br/>  this coupon code validate till [EXPIRY_DATE] <br/> Use the coupon code and enjoy your shopping with Sagar-co!</p>
                        <p>Thank you for your support!</p>
                        <p>Best wishes,</p>
                        <p>The Sagar-co Team</p>
                    </main>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Sagar-Services | Privacy Policy | Support</p>
                        <p>© 2024 Sagar-Services. All Rights Reserved.</p>
                    </footer>
                </div>
                </body>
                </html>
            """,
        "PASSWORD_CHANGE_TEMPLATE": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to Sagar-Services!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                        <img src="companyLogo.png" alt="Sagar-Services Logo" width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <main class="content" style="text-align: start; margin-bottom: 20px;">
                        <p>Hi [FIRST_NAME],</p>
                        <p>You have been succssfully changed your password.</p>
                        <p>Best Regards,</p>
                        <p>The Sagar-Services Team</p>
                    </main>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Sagar-Services | Privacy Policy | Support</p>
                        <p>© 2024 Sagar-Services. All Rights Reserved.</p>
                    </footer>
                </div>
                </body>
                </html>
            """,
        "BOOKING_THANK_YOU_TEMPLATE": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to Sagar-Services!</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div class="container" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); ">
                    <header class="header" style="text-align: start; margin-bottom: 20px;">
                        <img src="companyLogo.png" alt="Sagar-Services Logo" width="150px" height="50px" style="display: block; margin-right: auto;">
                    </header>
                    <main class="content" style="text-align: start; margin-bottom: 20px;">
                        <h1>Thank You for Choosing our Service!</h1>
                        <p>Hi [FULL_NAME],</p>
                        <p>We appreciate your recent booking and hope you had an exceptional service experience. Your feedback is important to us and helps us improve our services.</p>
                        <p>We kindly ask you to take a moment to share your thoughts on your recent shopping experience. Your input means a lot to us!</p>
                        <p>Thank you for your support!</p>
                        <p>Best wishes,</p>
                        <p>The Sagar-co Team</p>
                    </main>
                    <footer class="footer" style="text-align: center; margin-top: 20px;">
                        <p>Sagar-Services | Privacy Policy | Support</p>
                        <p>© 2024 Sagar-Services. All Rights Reserved.</p>
                    </footer>
                </div>
                </body>
                </html>
            """,
    }
)


"""
OTP
ACCOUNT CREATION
ORDER DELIVERY(SUCCESS)
ORDER CREATION +
    STATUS CHANGE
SERVICE BOOKED + 
    STATUS CHANGE
REVIEW ASKING EMAIL(ORDER,SERVICE BOOKING)
OFFER RELATED EMAIL 

INVOICE AFTER PAYMENT
"""
