import string

import Account.models
from Account.variables import Numbers as AccountMaxAndMinLengthStrings
from Account.variables import Strings as AccountModelVerboseNameStrings
from Account.variables import ErrorTexts as AccountValidationErrorStrings

slug_allowed_characters = string.ascii_letters + string.digits + "-" + "_"


def has_multiple_languages(value):
    persian_alphabet = "ءآأؤإئابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"

    has_english_chars = any(char in string.ascii_letters for char in value)
    has_persian_chars = any(char in persian_alphabet for char in value)

    return has_english_chars == has_persian_chars


def validate_mobile_phone_handler(mobile_phone, mobile_phone_exists_importance=True):
    has_errors = False
    message = None
    code = None

    mobile_phone_exists = Account.models.CustomUser.objects.filter(mobile_phone=mobile_phone).exists()

    if mobile_phone_exists_importance:
        if mobile_phone_exists:
            has_errors = True
            message = AccountValidationErrorStrings.already_exists(
                field_name=AccountModelVerboseNameStrings.mobile_phone)
            code = "already_exists"

    if not mobile_phone.isnumeric():
        has_errors = True
        message = AccountValidationErrorStrings.characters_not_allowed(
            field_name=AccountModelVerboseNameStrings.mobile_phone)
        code = "characters_not_allowed"

    elif len(mobile_phone) != AccountMaxAndMinLengthStrings.mobile_phone_max:
        has_errors = True
        message = AccountValidationErrorStrings.not_exact_length(
            exact_length=AccountMaxAndMinLengthStrings.mobile_phone_max,
            field_name=AccountModelVerboseNameStrings.mobile_phone, digit_or_char="digit")
        code = "not_exact_length"

    elif mobile_phone[0] != "0" or mobile_phone[1] != "9":
        has_errors = True
        message = AccountValidationErrorStrings.invalid_format(field_name=AccountModelVerboseNameStrings.mobile_phone)
        code = "invalid_format"

    elif len(set(mobile_phone)) < AccountMaxAndMinLengthStrings.mobile_phone_digits_variety_min:
        has_errors = True
        message = AccountValidationErrorStrings.invalid_format(field_name=AccountModelVerboseNameStrings.mobile_phone)
        code = "invalid_format"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_username_handler(username, username_exists_importance=True):
    has_errors = False
    message = None
    code = None

    username_exists = Account.models.CustomUser.objects.filter(username=username).exists()

    if username_exists_importance:
        if username_exists:
            has_errors = True
            message = AccountValidationErrorStrings.already_exists(field_name=AccountModelVerboseNameStrings.username)
            code = "already_exists"

    if len(username) < AccountMaxAndMinLengthStrings.username_min:
        has_errors = True
        message = AccountValidationErrorStrings.length_is_low(min_length=AccountMaxAndMinLengthStrings.username_min,
                                                              field_name=AccountModelVerboseNameStrings.username,
                                                              digit_or_char="char")
        code = "length_is_low"

    elif username.isnumeric():
        has_errors = True
        message = AccountValidationErrorStrings.at_least_one_letter(field_name=AccountModelVerboseNameStrings.username)
        code = "at_least_one_letter"

    for character_checker in username:
        if character_checker not in slug_allowed_characters:
            has_errors = True
            message = AccountValidationErrorStrings.username_contains_disallowed_characters
            code = "username_contains_disallowed_characters"
            break

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_passwords_handler(password, password_repeat):
    has_errors = False
    message = None
    code = None

    if password and password_repeat and password != password_repeat:
        has_errors = True
        message = AccountValidationErrorStrings.passwords_do_not_match
        code = "passwords_do_not_match"

    elif len(password) < AccountMaxAndMinLengthStrings.password_min:
        has_errors = True
        message = AccountValidationErrorStrings.length_is_low(min_length=AccountMaxAndMinLengthStrings.password_min,
                                                              field_name=AccountModelVerboseNameStrings.password,
                                                              digit_or_char="char")
        code = "length_is_low"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_landline_phone_handler(landline_phone):
    has_errors = False
    message = None
    code = None

    if not landline_phone.isnumeric():
        has_errors = True
        message = AccountValidationErrorStrings.characters_not_allowed(
            field_name=AccountModelVerboseNameStrings.landline_phone)
        code = "characters_not_allowed"

    if len(landline_phone) < AccountMaxAndMinLengthStrings.landline_min:
        has_errors = True
        message = AccountValidationErrorStrings.length_is_low(min_length=AccountMaxAndMinLengthStrings.landline_min,
                                                              field_name=AccountModelVerboseNameStrings.landline_phone,
                                                              digit_or_char="digit")
        code = "characters_not_allowed"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_national_id_handler(national_id):
    has_errors = False
    message = None
    code = None

    if not national_id.isnumeric():
        has_errors = True
        message = AccountValidationErrorStrings.characters_not_allowed(
            field_name=AccountModelVerboseNameStrings.national_id)
        code = "characters_not_allowed"

    elif len(national_id) != AccountMaxAndMinLengthStrings.national_id_max:
        has_errors = True
        message = AccountValidationErrorStrings.not_exact_length(
            exact_length=AccountMaxAndMinLengthStrings.national_id_max,
            field_name=AccountModelVerboseNameStrings.national_id, digit_or_char="digit")
        code = "not_exact_length"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_full_name_handler(full_name):
    has_errors = False
    message = None
    code = None

    if len(full_name) < AccountMaxAndMinLengthStrings.full_name_min:
        has_errors = True
        message = AccountValidationErrorStrings.length_is_low(min_length=AccountMaxAndMinLengthStrings.full_name_min,
                                                              field_name=AccountModelVerboseNameStrings.full_name,
                                                              digit_or_char='char')
        code = "length_is_low"

    elif not full_name.replace(" ", "").isalpha():
        has_errors = True
        message = AccountValidationErrorStrings.digits_not_allowed(field_name=AccountModelVerboseNameStrings.full_name)
        code = "digits_not_allowed"

    elif has_multiple_languages(value=full_name):
        has_errors = True
        message = AccountValidationErrorStrings.only_1_language(field_name=AccountModelVerboseNameStrings.full_name)
        code = "only_1_language"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_bank_card_number_handler(bank_card_number):
    has_errors = False
    message = None
    code = None

    if not bank_card_number.isnumeric():
        has_errors = True
        message = AccountValidationErrorStrings.characters_not_allowed(AccountModelVerboseNameStrings.bank_card_number)
        code = "characters_not_allowed"

    elif len(bank_card_number) != AccountMaxAndMinLengthStrings.bank_card_number_max:
        has_errors = True
        message = AccountValidationErrorStrings.not_exact_length(
            exact_length=AccountMaxAndMinLengthStrings.bank_card_number_max,
            field_name=AccountModelVerboseNameStrings.bank_card_number, digit_or_char="digit")
        code = "not_exact_length"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_email_handler(email):
    has_errors = False
    message = None
    code = None

    email_exists = Account.models.CustomUser.objects.filter(email=email).exists()

    if email_exists:
        has_errors = True
        message = AccountValidationErrorStrings.already_exists(field_name=AccountModelVerboseNameStrings.email)
        code = "already_exists"

    return {"has_errors": has_errors, "message": message, "code": code}


def validate_address_count_handler(address_count):
    has_errors = False
    message = None
    code = None

    if address_count >= AccountMaxAndMinLengthStrings.address_instance_max:
        has_errors = True
        message = AccountValidationErrorStrings.too_many_instances(
            max_instance=AccountMaxAndMinLengthStrings.address_instance_max,
            field_name=AccountModelVerboseNameStrings.address)
        code = "instance_is_too_much"

    return {"has_errors": has_errors, "message": message, "code": code}
