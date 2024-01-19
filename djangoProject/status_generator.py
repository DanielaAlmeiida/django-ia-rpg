import random as rd

def status_generator():

    status = 0
    lucky = rd.randint(1, 100)

    if lucky <= 40:
        status = rd.randint(10, 80)
    elif lucky <= 65:
        status = rd.randint(81, 130)
    elif lucky <= 80:
        status = rd.randint(131, 180)
    elif lucky <= 90:
        status = rd.randint(181, 220)
    elif lucky <= 95:
        status = rd.randint(221, 260)
    elif lucky <= 97:
        status = rd.randint(261, 300)
    elif lucky <= 99:
        status = rd.randint(301, 350)
    else:
        status = rd.randint(351, 500)

    return status