from .models import ModelPermission, PermissionModelRegistry

def has_model_permission(user, model_name, action):
    try:
        perm = ModelPermission.objects.select_related('permission_model').get(
            user=user,
            permission_model__model_name=model_name.lower()
        )
        return getattr(perm, f"can_{action}", False)
    except ModelPermission.DoesNotExist:
        return False
