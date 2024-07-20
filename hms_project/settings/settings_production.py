from hms_project.settings import *
import os
import environ


# environmet variable
    # 1- pip install python-dotenv
    # 2- Create a .env file In your project directory
    # 3- Define environment variables : 
    #     a- In the .env file, define your environment variables in the format "VARIABLE_NAME=variable_value"
    # 4- Load environment variables in settings.py :
        # import os
        # from dotenv import load_dotenv
        # load_dotenv()
    # Access environment variables in settings.py :
        # a- In your settings.py file, you can access the environment variables using os.getenv() :
        # b- SECRET_KEY = os.getenv('SECRET_KEY')
        #     DEBUG = os.getenv('DEBUG')
        #     DATABASE_URL = os.getenv('DATABASE_URL')


env = environ.Env()
env.read_env('.env')

SECRET_KEY = env('PRODUCTION_SECRET_KEY')

# Disable debug mode
DEBUG = env("DEBUG")


ALLOWED_HOSTS = []


# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


MIDDLEWARE += [
    # عبارة عن برمجية وسيطة توفرها حزمة WhiteNoise في Django. يتم استخدامه لخدمة الملفات الثابتة بكفاءة في الإنتاج
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

# Add production-specific authentication backends
AUTHENTICATION_BACKENDS += [
    # Production-specific authentication backends...
]

# Update logging configuration
LOGGING.update({
    # Production-specific logging configuration...
})
