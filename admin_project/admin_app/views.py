import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def admin_login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "status": "success",
                    "message": "Admin login successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "username": user.username
                }, status=200)
            else:
                return JsonResponse({
                    "status": "fail",
                    "message": "Invalid credentials or not an admin"
                }, status=401)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON"
            }, status=400)

    return JsonResponse({
        "status": "error",
        "message": "Only POST method allowed"
    }, status=405)




@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status": "success", "message": "Logout successful"})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=400)
