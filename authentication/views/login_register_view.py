
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.serializers import LoginSerializer,RegisterSerializer



class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  
            return Response(
                {
                    "status": "success",
                    "message": "Registration successful.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

       



class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True) 

            return Response(
                {"status": "success",
                "message": "Login successful.",
                "data": serializer.validated_data
                },
                status=status.HTTP_200_OK
            )
        
        