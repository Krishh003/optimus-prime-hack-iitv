from django.apps import AppConfig

class ListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listings'

    def ready(self):
        from .views import create_default_admin
        try:
            admin = create_default_admin()
            if admin:
                print("Default admin account is ready")
            else:
                print("Failed to create default admin account")
        except Exception as e:
            print(f"Error initializing default admin: {str(e)}")