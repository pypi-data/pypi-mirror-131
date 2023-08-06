code = ['ie', 'in', 'us']
dCode = ['+353', '+91', '+1']


def getPhoneNumber(number):
    if verifyPhoneNumber(number[2:]):
        for i in range(0, len(code)):
            if number[0:2].lower() == code[i]:
                print("1")
                number = (number.replace(number[0:2], dCode[i]))
    return number


def verifyPhoneNumber(number):
    if len(number) == 9:
        return True
    else:
        return False
