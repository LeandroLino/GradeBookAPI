import random

def generate_registration_id():
    base_number = random.randint(100000, 999999)
    digit = calculate_check_digit(base_number)
    return str(base_number) + str(digit)

def validate_registration_number(registration_number):
    if len(registration_number) != 7:
        return False

    base_number = int(registration_number[:6])
    provided_check_digit = int(registration_number[6])

    calculated_check_digit = calculate_check_digit(base_number)

    return provided_check_digit == calculated_check_digit


def calculate_check_digit(base_number):
    total = 0
    multiplier = 2

    for digit in reversed(str(base_number)):
        total += int(digit) * multiplier
        multiplier += 1
        if multiplier > 9:
            multiplier = 2

    remainder = total % 11
    if remainder < 2:
        calculated_check_digit = 0
    else:
        calculated_check_digit = 11 - remainder

    return calculated_check_digit
