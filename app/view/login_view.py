from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Person
from app.serializer.main_serializer import LoginModelSerializer


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginModelSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            try:
                user = Person.objects.get(phone_number=phone_number, password=password)
                # Authentication successful, implement your logic here
                return Response(data={"Message": "Successfully logged in"}, status=status.HTTP_200_OK)
            except Person.DoesNotExist:
                # User not found or authentication failed
                return Response(data={"Message": "Incorrect phone number or password"},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
