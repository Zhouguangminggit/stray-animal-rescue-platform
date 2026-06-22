from django.conf import settings


def site_context(request):
    return {
        "site_name": "守望小动物",
        "auth_style": settings.AUTH_STYLE,
        "auth_media": settings.AUTH_MEDIA,
    }
