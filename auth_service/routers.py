class AuthRouter:
    """
    Router to manage database operations for authentication and application-specific data.
    """

    def db_for_read(self, model, **hints):
        """Point database operations for read queries."""
        if model._meta.app_label == 'auth_service':
            return 'default'
        elif model._meta.app_label == 'system_a':
            return 'system_a'
        elif model._meta.app_label == 'system_b':
            return 'system_b'
        return None

    def db_for_write(self, model, **hints):
        """Point database operations for write queries."""
        if model._meta.app_label == 'auth_service':
            return 'default'
        elif model._meta.app_label == 'system_a':
            return 'system_a'
        elif model._meta.app_label == 'system_b':
            return 'system_b'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relationships only within the same app."""
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Decide on which database to run migrations."""
        if app_label == 'auth_service':
            return db == 'default'
        elif app_label == 'system_a':
            return db == 'system_a'
        elif app_label == 'system_b':
            return db == 'system_b'
        return None
