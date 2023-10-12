from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializer.login_serializer import LoginModelSerializer


class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginModelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response(data={"Message": "Successfully login"},
                            status=status.HTTP_200_OK)
        return Response(data={serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
