
from rest_framework import  status
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView




class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        # try:
            response = super().post(request, *args, **kwargs)  
            return Response(
                {
                    "status": "success",
                    "message": "Token refreshed successfully.",
                    "data": {
                          "token":response.data  
                    }
                },
                status=status.HTTP_200_OK
            )
        



class CustomTokenVerifyView(TokenVerifyView):
    """Custom Token Verify View to maintain response format consistency"""

    def post(self, request, *args, **kwargs):
        # try:
            response = super().post(request, *args, **kwargs)  
            return Response(
                {
                    "status": "success",
                    "message": "Token is valid.",
                },
                status=status.HTTP_200_OK
            )
    

