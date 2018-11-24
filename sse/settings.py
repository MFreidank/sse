from cbs.utils import as_list
import cbs
import os

class Base:
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': f'django.contrib.auth.password_validation.{validator}'}
        for validator in [
            'UserAttributeSimilarityValidator',
            'MinimumLengthValidator',
            'CommonPasswordValidator',
            'NumericPasswordValidator',
        ]
    ]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_ENGINE = cbs.env(None, key='DJANGO_DATABASE_ENGINE')
    DATABASE_NAME = cbs.env(None, key='DJANGO_DATABASE_NAME')
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'rest_framework',
        'sse',
        'sse.api',
        'sse.core',
    ]
    LANGUAGE_CODE = 'en-us'
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    REST_FRAMEWORK = {
       'DEFAULT_RENDERER_CLASSES': (
           'rest_framework.renderers.JSONRenderer',
        )
    }
    ROOT_URLCONF = 'sse.urls'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    @property
    def DATABASES(self):
        return {
            'default': {
                'ENGINE': self.DATABASE_ENGINE,
                'NAME': self.DATABASE_NAME,
            }
        }

    @cbs.env(key='DJANGO_MEDIA_ROOT')
    def MEDIA_ROOT(self):
        return os.path.join(self.BASE_DIR, 'media')

    @cbs.env(key='DJANGO_MEDIA_URL')
    def MEDIA_URL(self):
        return '/media/'

    @cbs.env(key='DJANGO_SECRET_KEY')
    def SECRET_KEY(self):
        return ''

    @cbs.env(key='DJANGO_STATIC_ROOT')
    def STATIC_ROOT(self):
        return os.path.join(self.BASE_DIR, 'static')

    @cbs.env(key='DJANGO_STATIC_URL')
    def STATIC_URL(self):
        return '/static/'


class API(Base):
    ROOT_URLCONF = 'api.urls'
    WSGI_APPLICATION = 'api.wsgi.application'


class Testing(Base):
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']


class Development(Testing):
    pass


MODE = os.environ['DJANGO_MODE']
cbs.apply(MODE, globals())
