EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mohit_saini@excellencetechnologies.info'
EMAIL_HOST_PASSWORD = 'vgflhrznpzvcvfqu'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


url_api = "(<a href =http://127.0.0.1:8000/set_pass/?Email={{DATA}}>Click Here To Chnage Password</a>)"