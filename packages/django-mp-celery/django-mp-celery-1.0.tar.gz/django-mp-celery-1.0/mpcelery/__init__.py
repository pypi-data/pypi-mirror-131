
from django.apps import AppConfig


def setup_settings(settings, is_prod, **kwargs):

    settings.update({
        'CELERY_BROKER_URL': 'redis://0.0.0.0:6379/0',
        'CELERY_RESULT_BACKEND': (
            'django_celery_results.backends.DatabaseBackend'),
        'CELERY_TIMEZONE': settings.get('TIMEZONE', 'Europe/Kiev')
    })

    extra_apps = [
        'django_celery_beat',
        'django_celery_results'
    ]

    installed_apps = settings['INSTALLED_APPS']

    for app in extra_apps:
        if app not in installed_apps:
            installed_apps.append(app)


class CeleryAppConfig(AppConfig):

    name = 'mpcelery'


default_app_config = 'mpcelery.CeleryAppConfig'
