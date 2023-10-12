from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializer.register_serializer import RegisterModelSerializer


class RegisterApiView(APIView):

    def post(self, request):
        serializer = RegisterModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"Message": "User successfully registered"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
