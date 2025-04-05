DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'sponsorship_db',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb://localhost:27017/',
            'port': 27017,
        }
    }
} 