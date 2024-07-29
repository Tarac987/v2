#session.py
class Session:
    def __init__(self, utilisateur):
        self.utilisateur = utilisateur
        self.permissions = self._get_permissions(utilisateur.role)

    def _get_permissions(self, role):
        permissions = {
            "admin": ["view_dashboard", "manage_users"],
            "employe": ["view_dashboard"]
        }
        return permissions.get(role, [])

    def has_permission(self, permission):
        return permission in self.permissions
