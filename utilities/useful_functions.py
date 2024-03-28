import os
import secrets
import string


def generate_token(token_length):
    url_safe_alphabet = string.ascii_letters + string.digits + '-_~'
    url_safe_password = ''.join(secrets.choice(url_safe_alphabet) for i in range(token_length))
    return url_safe_password


def humanize_video_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def duration_hour_to_seconds(duration_str):
    hours, minutes, seconds = map(int, duration_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def get_file_size(file_path):
    return os.path.getsize(file_path)
