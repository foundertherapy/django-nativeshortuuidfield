SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    "tests",
]

# # Database
# # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
