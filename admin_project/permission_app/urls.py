# from django.urls import path
# from .views import (
#     ListAllModelPermissions,
#     UserPermissionsDetail,
#     PermissionUserListByCodename,
#     UsersByPermissionType,
#     AssignOrRemovePermission,
#     PermissionUserListByModel,
#     MyPermissionSummaryView,
#     AdminUsersByPermissionType,
#     CheckUserModelPermission,
#     UserModelPermissionsAPIView,
#     WebinarListCreateView,
#     WebinarRetrieveUpdateDestroyView,
#     WebinarCreateView,
#     WebinarUpdateView,
#     WebinarDeleteView,
# )

# urlpatterns = [
#     # Permissions
#     path('permissions/all/', ListAllModelPermissions.as_view(), name='list-all-permissions'),
#     path('permissions/user/<str:username>/', UserPermissionsDetail.as_view(), name='user-permissions-detail'),
#     path('permissions/by_codename/<str:codename>/', PermissionUserListByCodename.as_view(), name='permission-user-list'),
#     path('permissions/by_type/<str:model_name>/<str:perm_type>/', UsersByPermissionType.as_view(), name='users-by-permission-type'),
#     path('permissions/model/<str:model_name>/<str:codename>/', PermissionUserListByModel.as_view(), name='permission-user-list-by-model'),
#     path('permissions/assign-remove/', AssignOrRemovePermission.as_view(), name='assign-remove-permission'),
#     path('permissions/', UserModelPermissionsAPIView.as_view(), name='user_model_permissions'),
#     path('check/<str:model_name>/<str:permission_action>/', CheckUserModelPermission.as_view(), name='check-user-permission'),
#     path('permissions/filter/', AdminUsersByPermissionType.as_view(), name='permission-filter-by-model'),
#     path('permissions/my-permissions/', MyPermissionSummaryView.as_view(), name='my-permissions'),

#     # Webinars
#     path('webinars/', WebinarListCreateView.as_view(), name='webinar-list-create'),
#     path('webinars/<int:pk>/', WebinarRetrieveUpdateDestroyView.as_view(), name='webinar-detail'),
#     path('webinars/create/', WebinarCreateView.as_view(), name='webinar-create'),
#     path('webinars/<int:pk>/update/', WebinarUpdateView.as_view(), name='webinar-update'),
#     path('webinars/<int:pk>/delete/', WebinarDeleteView.as_view(), name='webinar-delete'),
# ]

from django.urls import path
from .views import (
    # Webinar views
    WebinarListCreateView,
    WebinarDetailView,

    # Permission management views
    ListAllModelPermissions,
    UserPermissionsDetail,
    PermissionUserListByCodename,
    UsersByPermissionType,
    AssignOrRemovePermission,
    PermissionUserListByModel,
    # MyPermissionSummaryView,
    AdminUsersByPermissionType,
    CheckUserModelPermission,
    UserModelPermissionsAPIView,
    CustomModelPermissionAPIView
)

urlpatterns = [
    #  Webinar endpoints
    path('webinars/', WebinarListCreateView.as_view(), name='webinar-list-create'),
    path('webinars/<int:pk>/', WebinarDetailView.as_view(), name='webinar-detail'),

    # Permission-related endpoints
    path('permissions/all/', ListAllModelPermissions.as_view(), name='list-all-permissions'),
    path('permissions/user/<str:username>/', UserPermissionsDetail.as_view(), name='user-permissions-detail'),
    path('permissions/by_codename/<str:codename>/', PermissionUserListByCodename.as_view(), name='permission-user-list'),
    path('permissions/by_type/<str:model_name>/<str:perm_type>/', UsersByPermissionType.as_view(), name='users-by-permission-type'),
    path('permissions/model/<str:model_name>/<str:codename>/', PermissionUserListByModel.as_view(), name='permission-user-list-by-model'),
    path('permissions/assign-remove/', AssignOrRemovePermission.as_view(), name='assign-remove-permission'),
    path('permissions/', UserModelPermissionsAPIView.as_view(), name='user_model_permissions'),
    path('check/<str:model_name>/<str:permission_action>/', CheckUserModelPermission.as_view(), name='check-user-permission'),
    path('pepermissions/my-permissions/rmissions/filter/', AdminUsersByPermissionType.as_view(), name='permission-filter-by-model'),
    # path('', MyPermissionSummaryView.as_view(), name='my-permissions'),
     path('permissions/custom/', CustomModelPermissionAPIView.as_view(), name='custom-user-permissions'),
    
]
