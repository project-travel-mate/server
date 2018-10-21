# Email template signature
EMAIL_SIGNATURE = """
--
Team Project Travel Mate
Made open source with ❤️ and coffee at https://github.com/project-travel-mate

Buy us a ☕ to keep us stayed fueled up at https://www.buymeacoffee.com/qITGMWB
"""

# User welcome mails
WELCOME_MAIL_SUBJECT = "Welcome {0} to Travel Mate!"
WELCOME_MAIL_CONTENT = """
Welcome {0},
Thank you for registering with us.

""" + EMAIL_SIGNATURE

# Forgot password mails
FORGOT_PASSWORD_MAIL_SUBJECT = "Travel Mate - Password reset request"
FORGOT_PASSWORD_MAIL_CONTENT = """
Dear {0},

You have requested a password reset for your travel mate account. Use code {1} to reset your password.
If you didn't make this request, ignore this email.
""" + EMAIL_SIGNATURE

# Verification code mails
VERIFICATION_CODE_MAIL_SUBJECT = "Travel Mate - Your Verification Code"
VERIFICATION_CODE_MAIL_CONTENT = """
Dear {0},

Your verification code: {1}
""" + EMAIL_SIGNATURE
