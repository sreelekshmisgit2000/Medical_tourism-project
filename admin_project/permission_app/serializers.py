

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Webinar, ModelPermission, PermissionModelRegistry

User = get_user_model()

class PermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class ContentTypePermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = ContentType
        fields = ['app_label', 'model', 'permissions']

    def get_permissions(self, obj):
        perms = Permission.objects.filter(content_type=obj)
        return PermissionListSerializer(perms, many=True).data


class UserPermissionViewSerializer(serializers.ModelSerializer):
    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'user_permissions']

    def get_user_permissions(self, obj):
        request_user = self.context['request'].user
        if request_user.is_superuser or request_user == obj:
            permissions = obj.user_permissions.all()
            return PermissionListSerializer(permissions, many=True).data
        return []


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPermission
        fields = '__all__'


class ModelPermissionListSerializer(serializers.Serializer):
    permissions_by_model = serializers.SerializerMethodField()

    def get_permissions_by_model(self, user):
        user = self.context['request'].user
        permissions = ModelPermission.objects.filter(user=user)
        result = {}

        for perm in permissions:
            model_key = perm.permission_model.model_name.lower()
            actions = []
            if perm.can_create:
                actions.append('add_' + model_key)
            if perm.can_read:
                actions.append('view_' + model_key)
            if perm.can_update:
                actions.append('change_' + model_key)
            if perm.can_delete:
                actions.append('delete_' + model_key)
            result[model_key] = actions
        return result


class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = '__all__'



class CustomModelPermissionSerializer(serializers.Serializer):
    permissions_by_model = serializers.SerializerMethodField()

    def get_permissions_by_model(self, obj):
        user = self.context['request'].user
        result = {}

        # Get all ModelPermission objects for the current user
        user_permissions = ModelPermission.objects.filter(user=user)

        for perm in user_permissions:
            model_name = perm.permission_model.model_name.lower()
            actions = []

            if perm.can_create:
                actions.append(f"add_{model_name}")
            if perm.can_read:
                actions.append(f"view_{model_name}")
            if perm.can_update:
                actions.append(f"change_{model_name}")
            if perm.can_delete:
                actions.append(f"delete_{model_name}")

            result[model_name] = actions

        return result
