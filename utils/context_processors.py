from Us.models import SocialMedia, AboutUs


def social_media(request):
    social_media = SocialMedia.objects.last()
    about_us = AboutUs.objects.last()

    context = {
        'social_media': social_media,
        'about_us': about_us,
    }

    return context
