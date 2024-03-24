class BaseErrorTexts:
    not_null = "همه مقادیر فرم کامل پر نشده است!"
    successful_action = "عملیات با موفقیت انجام شد."

    @staticmethod
    def length_is_low(min_length, field_name, digit_or_char):
        if digit_or_char == 'char':
            return f'{field_name} باید حداقل {min_length} کاراکتر داشته باشد.'
        else:
            return f'{field_name} باید حداقل {min_length} رقم داشته باشد.'

    @staticmethod
    def digits_not_allowed(field_name):
        return f'{field_name} نمی‌تواند شامل رقم باشد.'

    @staticmethod
    def characters_not_allowed(field_name):
        return f'{field_name} نمی‌تواند شامل کاراکتر باشد.'

    @staticmethod
    def only_1_language(field_name):
        return f'{field_name} فقط می‌تواند شامل یک زبان باشد.'

    @staticmethod
    def not_exact_length(exact_length, field_name, digit_or_char):
        if digit_or_char == 'char':
            return f'{field_name} فقط می‌تواند {exact_length} کاراکتر داشته باشد.'
        else:
            return f'{field_name} فقط می‌تواند {exact_length} رقم داشته باشد.'

    @staticmethod
    def already_exists(field_name):
        return f' این {field_name} قبلا ثبت شده است.'

    @staticmethod
    def invalid_format(field_name, extra_information=None):
        if extra_information is None:
            return f'{field_name} نامعتبر است.'
        else:
            return f'{field_name} ({extra_information})'

    @staticmethod
    def at_least_one_letter(field_name):
        return f'{field_name} باید حداقل یک حرف انگلیسی داشته باشد.'

    @staticmethod
    def start_or_end_not_valid(field_name, exclude, start_with_or_end_with):
        if start_with_or_end_with == 'start_with':
            return f'{field_name} نمی‌تواند با {exclude} شروع شود.'
        else:
            return f'{field_name} نمی‌تواند با {exclude} تمام شود.'

    @staticmethod
    def too_many_instances(max_instance, field_name):
        return f'تعداد {field_name}‌ها نمی‌تواند بیشتر از {max_instance} مورد باشد.'

    @staticmethod
    def field_range_limit(number, field_name, pos_or_neg):
        if pos_or_neg == 'pos':
            return f'مقدار {field_name} نمی‌تواند بیشتر از {number} باشد.'
        else:
            return f'مقدار {field_name} نمی‌تواند کمتر از {number} باشد.'

    @staticmethod
    def only_one_field(*args):
        text = "لطفاً فقط یکی از فیلد‌های "
        for i, arg in enumerate(args):
            text += f' "{arg}"'
            if i < len(args) - 2:
                text += '، '
            elif i == len(args) - 2:
                text += ' و '

        text += " را انتخاب کنید."
        return text

    @staticmethod
    def necessary_fields(field_name):
        return f'{field_name} ضروری است.'

    @staticmethod
    def does_not_exist(field_name):
        return f'این {field_name} در دیتابیس وجود ندارد.'

    @staticmethod
    def not_all_filds(field_name):
        return f'فقط فیلد های ظروروی را پر کنید'

    @staticmethod
    def successful_job(job):
        return f'{job} با موفقیت انجام شد.'

    @staticmethod
    def unsuccessful_job(job):
        return f'{job} با خطا مواجه شد.'

    @staticmethod
    def negatives_not_allowed(field_name):
        return f"فیلد {field_name} نباید مقدار منفی داشته باشد!"

    @staticmethod
    def values_not_allowed(field_name):
        return f"مقدار{field_name}نمیتواند متفاوت باشد"


class BaseStrings:
    slug = 'اسلاگ (متن داخل URL)'
    needed = 'ضروری'
    created_at = 'ایجاد شده در تاریخ'
    updated_at = 'ویرایش شده در تاریخ'
    deleted_at = 'حذف شده در تاریخ'
    mobile_phone = 'شماره تلفن همراه'
    landline_phone = 'شماره تلفن ثابت'
    email = 'آدرس ایمیل'
    can_be_shown = 'مجوز نشان داده شدن دارد؟'
    image = 'تصویر'
    mobile_image = 'تصویر برای حالت موبایل'
    desktop_image = 'تصویر برای حالت دسکتاپ'
    images = 'تصاویر'
    parent = 'والد'
    tags = 'تگ‌ها'
    title = 'تیتر'
    full_name = 'اسم'
    description = 'توضیحات'
    uuid = 'آیدی (فرمت uuid)'
    name = 'نام'
    barcode = 'بارکد'
    reason = 'علت'
    file = 'فایل'
    link = 'لینک'
    body = 'بدنه'
    type = 'نوع'
    label = 'برچسب'
    property = 'ویژگی'
    is_available_in_stock = 'آیا در انبار موجود است؟'
    available_in_stock_count = 'تعداد موجود در انبار'
    date = 'تاریخ'
    auto_generated = 'خودکار ایجاد خواهد شد'
    user_status = 'وضعیت کاربر معمولی'
    admin_status = 'وضعیت ادمین'
    is_valid = 'آیا معتبر است؟'
    quantity = "تعداد"
    default = "پیش فرض"


class BaseNumbers:
    uuid_4_token_max = 36
    landline_phone_max = 15
    mobile_phone_max = 11
    mobile_phone_min = 11
    email_max = 255
    name_max = 100
    name_slug_max = name_max * 2
    title_max = 75
    title_slug_max = title_max * 2
    description_max = 10000
    body_max = 1000
    label_max = 50
    address_max = 1000
    address_instance_max = 6
    property_max = 1000
    per_page_pagination_max = 20
    status_max = 50
    barcode_max = 9999999
    barcode_min = 1000000


class ErrorStrings(BaseErrorTexts):
    empty_search_query_not_allowed = 'یک عبارت برای جست‌و‌جو وارد کنید.'


class Strings(BaseStrings):
    hero_banner = 'هیرو بنر'
    hero_banners = 'هیرو بنر‌ها'
    fist_banner = 'بنر پایین دست راست'
    first_banners = 'بنرهای پایین دست راست'
    second_banner = 'بنر پایین دست چپ'
    second_banners = 'بنرهای پایین دست چپ'
    home = 'خانه'


class MediaPaths:
    hero_banner_files = 'home/hero-banner/image/files'


class Numbers(BaseNumbers):
    pass
