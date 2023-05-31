import random

#class password to represnt passwords in account.
class Password:
    def __init__(self, Url, password, Owner):
        self.url = Url
        self.password = password
        self.owner = Owner

    #a function to generate a random password.
    def randomPass(self, len, specialChars):
        password = ''
        for i in range(len):
            password += random.choice(specialChars)
        self.password = password
        return password