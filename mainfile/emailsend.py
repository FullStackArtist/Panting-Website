import smtplib
class emailsend:
    def __init__(self):
        self.val=["email"]
   
    def sent(self,full_name,address,email,phone_number,descrption):
        message="your painting will ready sonn within few days"
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("############@gmail.com","##########")
        server.sendmail("############@gmail.com",email,message)
        return "mail sent "
         
