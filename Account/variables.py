from Home.variables import BaseStrings, BaseNumbers, BaseErrorTexts


class ErrorTexts(BaseErrorTexts):
    only_available_with_mobile_phone = 'کاربر باید شماره تلفن داشته باشد.'
    only_available_with_username = 'کاربر باید نام کاربری داشته باشد.'
    mobile_phone_index_0_is_not_zero = 'شماره تلفن همراه با 0 شروع نشده است.'
    landline_phone_index_0_is_not_zero = 'شماره تلفن ثابت با 0 شروع نشده است.'
    is_staff_must_be_true_for_staff = 'کارمند باید مقدار "is_staff=True" را داشته باشد.'
    is_staff_must_be_true_for_super_user = 'ابر کاربر باید مقدار "is_staff=True" را داشته باشد.'
    username_contains_disallowed_characters = 'نام کاربری فقط می‌تواند شامل حروف انگلیسی، ارقام، "-"و "_" باشد.'
    log_in_first = 'ابتدا وارد حساب کاربری خود شوید.'
    access_denied_for_this_page = "شما اجازه دسترسی به این صفحه را ندارید."
    staff_only = 'این بخش فقط مخصوص ادمین سایت است.'
    non_staff_only = 'این بخش فقط مختص به کاربران معمولی است.'
    sms_code_invalid = 'این کد تأیید نامعتبر است.'
    no_accounts_were_found = 'هیچ حساب کاربری با این مشخصات یافت نشد.'
    passwords_do_not_match = 'رمز عبور‌ها با یکدیگر هم‌خوانی ندارند!'


class Strings(BaseStrings):
    username = 'نام کاربری'
    user = 'کاربر'
    admin = 'ادمین'
    is_staff = 'آیا کارمند است؟'
    is_active = 'آیا فعال است؟'
    date_joined = 'تاریخ پیوستن'
    password = 'رمز عبور'
    password_repeat = 'تکرار رمز عبور'
    sms_code = 'کد پیامک شده'
    token = 'توکن'
    full_name = 'نام و نام خانوادگی'
    national_id = 'کد ملی'
    bank_card_number = 'شماره کارت بانکی'
    profile_image = 'تصویر پروفایل'
    is_user_loyal = 'آیا کاربر عمده است؟'
    is_user_stockman = 'آیا کاربر انباردار است؟'
    is_user_accountants = 'آیا کاربر حسابدار است؟'
    is_user_visitor = 'آیا کاربر ویزیتور است؟'
    is_user_repairman = 'آیا کاربر تعمیرکار است؟'
    is_user_ticket_responder = 'آیا کاربر پاسخگوی تیکت است؟'
    register_mode_en = "register_mode"
    register_mode_fa = "حالت ثبت نام"
    forget_password_mode_en = "forget_password"
    forget_password_mode_fa = "حالت فراموشی رمز عبور"
    delete_account_mode_en = "delete_account_mode"
    delete_account_mode_fa = "حالت حذف حساب کاربری"
    custom_user = 'کاربر'
    custom_users = 'کاربران'
    otp = 'اُ-تی-پی'
    otp_plural = 'اُ-تی-پی‌ها'
    custom_user_extra_information = 'اطلاعات اضافی کاربر'
    custom_user_extra_information_plural = 'اطلاعات اضافی کاربران'
    app_name = 'حساب کاربری'
    verification_code = 'کد تأیید'
    mobile_phone_or_username = 'شماره تلفن همراه یا نام کاربری'
    address = 'آدرس'
    addresses = 'آدرس‌ها'
    address_deletion = 'حذف آدرس'
    address_creation = 'ایجاد آدرس'
    password_change = 'تغییر رمز عبور'
    city = 'شهر'
    state = 'استان'
    biography = 'بیوگرافی'
    authentication_token = 'کد احراز هویت'
    cheque_date = "تاریخ چک"
    cheque_price = "مبلغ چک"
    cheque_number = "شماره چک"
    payment_state = "وضعیت مالی کاربر"
    account_creation = "ساخت حساب کاربری"
    visitor = "ویزیتور"
    is_user_cheque = "ایا کاربر چکی است"
    max_credit = "حداکثر اعتبار کاربر"


class MediaPaths:
    custom_user_extra_information_profile_image = 'account/custom-user-extra-information/image/images'

    custom_user_extra_information_default_profile_image = 'assets/images/profile.png'


class Numbers(BaseNumbers):
    username_max = 50
    username_min = 2
    city_max = 50
    username_slug_max = username_max * 2
    full_name_max = 50
    full_name_min = 5
    password_max = 100
    password_min = 4
    sms_code_max = 6
    otp_type_max = 50
    national_id_max = 10
    bank_card_number_max = 16
    sms_code_random_min = 100000
    sms_code_random_max = 999999
    mobile_phone_or_username_max = 50
    mobile_phone_digits_variety_min = 3
    biography_max = 1000
    landline_min = 5
