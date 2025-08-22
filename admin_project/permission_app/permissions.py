from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import ModelPermission, PermissionModelRegistry

User = get_user_model()

# ✅ Action mapping
ACTION_MAP = {
    "add": "can_create",
    "create": "can_create",
    "post": "can_create",          # ✅ Add this
    "view": "can_read",
    "read": "can_read",
    "get": "can_read",             # ✅ Add this
    "change": "can_update",
    "update": "can_update",
    "put": "can_update",           # ✅ Add this
    "patch": "can_update",         # ✅ Add this
    "delete": "can_delete"
}


# ✅ Get permissions user has (Django default system)
def get_user_model_permissions(user):
    user_permissions = user.user_permissions.all() | Permission.objects.filter(group__user=user)
    permission_dict = {}

    for perm in user_permissions:
        app_label = perm.content_type.app_label
        model = perm.content_type.model
        action = (
            'can_create' if perm.codename.startswith('add_') else
            'can_update' if perm.codename.startswith('change_') else
            'can_delete' if perm.codename.startswith('delete_') else
            'can_read' if perm.codename.startswith('view_') else
            perm.codename
        )

        permission_dict.setdefault(app_label, {}).setdefault(model, []).append(action)

    return permission_dict

# ✅ Get all model-level permissions from Django’s default system
def get_all_models_permissions():
    permissions = Permission.objects.select_related("content_type")
    data = {}

    for perm in permissions:
        app_label = perm.content_type.app_label
        model = perm.content_type.model
        codename = perm.codename

        data.setdefault(app_label, {}).setdefault(model, {
            "can_create": None,
            "can_update": None,
            "can_delete": None,
            "can_read": None
        })

        if codename.startswith("add_"):
            data[app_label][model]["can_create"] = perm.id
        elif codename.startswith("change_"):
            data[app_label][model]["can_update"] = perm.id
        elif codename.startswith("delete_"):
            data[app_label][model]["can_delete"] = perm.id
        elif codename.startswith("view_"):
            data[app_label][model]["can_read"] = perm.id

    return data

# ✅ Custom table-based permission check
def has_custom_permission(user, model_name, action):
    try:
        permission_model = PermissionModelRegistry.objects.get(model_name=model_name.lower())
        model_permission = ModelPermission.objects.get(user=user, permission_model=permission_model)

        perm_field = ACTION_MAP.get(action.lower())
        if not perm_field:
            return False  # Invalid or unmapped action

        return getattr(model_permission, perm_field, False)

    except (PermissionModelRegistry.DoesNotExist, ModelPermission.DoesNotExist, AttributeError):
        return False


# ✅ DRF Permission class - supports both method-based & action-based permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
class HasModelPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        # Dynamically get model_name and app_label from the queryset model
        model_cls = getattr(view.queryset, 'model', None)
        if model_cls is None:
            return False

        model_name = model_cls._meta.model_name
        app_label = model_cls._meta.app_label

        method = request.method
        action = getattr(view, 'action', None)

        if method in SAFE_METHODS:
            return user.has_perm(f'{app_label}.view_{model_name}')
        elif method == 'POST':
            return user.has_perm(f'{app_label}.add_{model_name}')
        elif method in ['PUT', 'PATCH']:
            return user.has_perm(f'{app_label}.change_{model_name}')
        elif method == 'DELETE':
            return user.has_perm(f'{app_label}.delete_{model_name}')
        elif action:
            codename = {
                'create': 'add',
                'list': 'view',
                'retrieve': 'view',
                'update': 'change',
                'partial_update': 'change',
                'destroy': 'delete',
            }.get(action)

            if codename:
                return user.has_perm(f'{app_label}.{codename}_{model_name}')

        return False


# ✅ Strict permission using custom table model
class StrictWebinarPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        action = request.method
        return has_custom_permission(request.user, "webinar", action.lower())

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)  # Same logic reused


class HasWebinarPermission(BasePermission):
    """
    Custom permission to check user has appropriate webinar permissions.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Map HTTP method to permission codename
        perms_map = {
            'GET': 'webinar_app.view_webinar',
            'POST': 'webinar_app.add_webinar',
            'PUT': 'webinar_app.change_webinar',
            'PATCH': 'webinar_app.change_webinar',
            'DELETE': 'webinar_app.delete_webinar',
        }

        required_permission = perms_map.get(request.method)
        if required_permission:
            return user.has_perm(required_permission)
        return False
