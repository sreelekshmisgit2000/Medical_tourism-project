from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from webinar_app.models import Webinar
from webinar_app.serializers import WebinarSerializer
from permission_app.models import ModelPermission
from permission_app.serializers import (
    ContentTypePermissionSerializer,
    ModelPermissionListSerializer,
    CustomModelPermissionSerializer
)
from permission_app.permissions import HasModelPermission, StrictWebinarPermission
from rest_framework.exceptions import PermissionDenied
from .permissions import has_custom_permission
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from hospital_reviews.models import Review
from hospital_reviews.serializers import ReviewSerializer



User = get_user_model()

# Webinar Views
class WebinarListCreateView(generics.ListCreateAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [StrictWebinarPermission]
    authentication_classes = [JWTAuthentication]


class WebinarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [StrictWebinarPermission]
    authentication_classes = [JWTAuthentication]


class WebinarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        webinar = super().get_object()
        action = self.request.method.upper()

        if action == 'GET' and not has_custom_permission(self.request.user, 'webinar', 'read'):
            raise PermissionDenied("You do not have permission to view this webinar.")
        if action == 'PUT' and not has_custom_permission(self.request.user, 'webinar', 'update'):
            raise PermissionDenied("You do not have permission to update this webinar.")
        if action == 'DELETE' and not has_custom_permission(self.request.user, 'webinar', 'delete'):
            raise PermissionDenied("You do not have permission to delete this webinar.")

        return webinar

    def update(self, request, *args, **kwargs):
        if not has_custom_permission(request.user, 'webinar', 'update'):
            return Response({"detail": "You do not have permission to update."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not has_custom_permission(request.user, 'webinar', 'delete'):
            return Response({"detail": "You do not have permission to delete."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class WebinarViewSet(viewsets.ModelViewSet):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [IsAuthenticated, HasModelPermission]




# Permission Inspection Views
class CheckUserModelPermission(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, model_name, permission_action):
        try:
            content_type = ContentType.objects.get(model=model_name)
            codename = f"{permission_action}_{model_name}"
            has_permission = request.user.has_perm(f"{content_type.app_label}.{codename}")
            return Response({
                "user": request.user.username,
                "model": model_name,
                "permission": codename,
                "has_permission": has_permission
            })
        except ContentType.DoesNotExist:
            return Response({"error": f"Model '{model_name}' not found."}, status=400)


# Admin Permission Assignments
class AssignOrRemovePermission(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        username = request.data.get('username')
        codename = request.data.get('permission_codename')
        action = request.data.get('action')

        if not username or not codename or action not in ['add', 'remove']:
            return Response({"error": "username, permission_codename, and action are required."}, status=400)

        try:
            user = User.objects.get(username=username)
            permission = Permission.objects.get(codename=codename)

            if action == 'add':
                user.user_permissions.add(permission)
                message = f"Permission '{codename}' assigned to {user.username}"
            else:
                user.user_permissions.remove(permission)
                message = f"Permission '{codename}' removed from {user.username}"

            return Response({"message": message})

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
        except Permission.DoesNotExist:
            return Response({"error": "Permission not found."}, status=404)


class ListAllModelPermissions(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        content_types = ContentType.objects.all()
        serializer = ContentTypePermissionSerializer(content_types, many=True)
        return Response(serializer.data)


class UserPermissionsDetail(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        permissions_by_model = {}
        model_perms = ModelPermission.objects.filter(user=user)

        for mp in model_perms:
            model = mp.permission_model.model_name.lower()
            actions = []
            if mp.can_create:
                actions.append("add_" + model)
            if mp.can_read:
                actions.append("view_" + model)
            if mp.can_update:
                actions.append("change_" + model)
            if mp.can_delete:
                actions.append("delete_" + model)
            permissions_by_model[model] = actions

        return Response({
            "username": user.username,
            "permissions_by_model": permissions_by_model
        })


class PermissionUserListByCodename(APIView):
    def get(self, request, codename):
        try:
            permission = Permission.objects.get(codename=codename)
            users = permission.user_set.all()
            data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return Response({'users_with_permission': data})
        except Permission.DoesNotExist:
            return Response({'error': 'Permission not found'}, status=404)


class PermissionUserListByModel(APIView):
    def get(self, request, model_name, codename):
        try:
            ct = ContentType.objects.get(model=model_name)
            perm = Permission.objects.get(content_type=ct, codename=codename)
            users = User.objects.filter(user_permissions=perm)
            data = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
            return Response(data)
        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            return Response({"error": "Permission not found"}, status=404)


class UsersByPermissionType(APIView):
    def get(self, request, model_name, perm_type):
        if not request.user.is_superuser:
            return Response({'error': 'Only admin can access'}, status=403)

        permissions = Permission.objects.filter(
            content_type__model=model_name.lower(),
            codename__startswith=perm_type
        )
        result = {
            perm.codename: [
                {'username': u.username, 'email': u.email}
                for u in perm.user_set.all()
            ]
            for perm in permissions
        }
        return Response(result)


class AdminUsersByPermissionType(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        model_name = request.query_params.get('model_name')
        permission_type = request.query_params.get('permission_type')

        if not model_name or not permission_type:
            return Response({"error": "model_name and permission_type required"}, status=400)

        codename = f"{permission_type}_{model_name}"
        try:
            content_type = ContentType.objects.get(model=model_name.lower())
            permission = Permission.objects.get(content_type=content_type, codename=codename)
            users = User.objects.filter(user_permissions=permission).distinct()
            return Response([
                {"id": u.id, "username": u.username, "email": u.email}
                for u in users
            ])
        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            return Response({"error": "Permission not found"}, status=404)


# User Self-Permission Summary
class CustomModelPermissionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomModelPermissionSerializer({}, context={'request': request})
        return Response({
            "username": request.user.username,
            "permissions_by_model": serializer.data['permissions_by_model']
        })


class UserModelPermissionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ModelPermissionListSerializer(context={'request': request})
        data = {
            "username": request.user.username,
            "permissions_by_model": serializer.get_permissions_by_model(request.user)
        }
        return Response(data, status=status.HTTP_200_OK)
