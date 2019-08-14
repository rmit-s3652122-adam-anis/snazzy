from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        """
        Safe imports for create profile function
        """
        import users.signals
