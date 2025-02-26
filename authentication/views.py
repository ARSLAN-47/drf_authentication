
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from authentication.serializers import LoginSerializer,RegisterSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError





class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()  

            return Response(
                {
                    "status": "success",
                    "message": "Registration successful.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
             return Response(
                    {
                    "status": "error", 
                    "message": "Validation failed.",
                    "errors": e.detail
                    }, 
                status=e.status_code
            )
        

        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": "An unexpected error occurred. Please try again later.",
                    # "errors": {"detail": str(e)}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class LoginView(APIView):
    def post(self, request):
        try:
            print("in login")
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True) 

            return Response(
                {"status": "success",
                "message": "Login successful.",
                "data": serializer.validated_data
                },
                status=status.HTTP_200_OK
            )
        
        except serializers.ValidationError as e:  
            return Response(
                    {
                    "status": "error", 
                    "message": "Validation failed.",
                    "errors": e.detail
                    }, 
                status=e.status_code
            )
        
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": "An unexpected error occurred. Please try again later.",
                    # "errors": {"detail": str(e)}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        






class CustomTokenRefreshView(TokenRefreshView):
    """Custom Refresh Token View to maintain response format consistency"""

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)  # Call default refresh logic
            return Response(
                {
                    "status": "success",
                    "message": "Token refreshed successfully.",
                    "data": response.data  # Token data from the parent class
                },
                status=status.HTTP_200_OK
            )
        except InvalidToken as e:
            return Response(
                {
                    "status": "error",
                    "message": "Invalid or expired refresh token.",
                    "errors": {"token": e.args[0]}  # JWT errors are passed in args[0]
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except TokenError as e:
            return Response(
                {
                    "status": "error",
                    "message": "Token error occurred.",
                    "errors": {"token": e.args[0]}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": "An unexpected error occurred. Please try again later.",
                    # "errors": {"detail": [str(e)]}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomTokenVerifyView(TokenVerifyView):
    """Custom Token Verify View to maintain response format consistency"""

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)  # Call default verify logic
            return Response(
                {
                    "status": "success",
                    "message": "Token is valid.",
                    # "data": response.data
                },
                status=status.HTTP_200_OK
            )
        except InvalidToken as e:
            return Response(
                {
                    "status": "error",
                    "message": "Invalid or expired token.",
                    "errors": {"token": e.args[0]}
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except TokenError as e:
            return Response(
                {
                    "status": "error",
                    "message": "Token verification failed.",
                    "errors": {"token": e.args[0]}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": "An unexpected error occurred. Please try again later.",
                    # "errors": {"detail": [str(e)]}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
