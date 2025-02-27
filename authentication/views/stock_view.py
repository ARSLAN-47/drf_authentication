
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.serializers import StockSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.constants import dummy_response

class StockView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):

            stock_name = request.query_params.get("stock_name")
            date = request.query_params.get("date")

            serializer = StockSerializer(data={"stock_name": stock_name, "date": date})
            serializer.is_valid(raise_exception=True)
            return Response(
                    {
                    "status": "success", 
                    "message": "Record Found",
                    "date": dummy_response
                    },
                    status=status.HTTP_200_OK
            )
        
       














#  except serializers.ValidationError as e:  
#             return Response(
#                     {
#                     "status": "error", 
#                     "detail": "Validation failed.",
#                     "messages": e.detail
#                     }, 
#                 status=e.status_code
#             )

#         except Exception as e:
#             return Response(
#                 {
#                     "status": "error",
#                     "detail": "An unexpected error occurred. Please try again later.",
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )







