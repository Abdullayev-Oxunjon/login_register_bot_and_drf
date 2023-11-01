from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Person, Group
from app.serializer.main_serializer import PersonModelSerializer


class GroupListCreateAPIView(ListCreateAPIView):
    queryset = Group.objects.all()


class PersonListCreateAPIView(ListCreateAPIView):
    serializer_class = PersonModelSerializer

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        # Get the group object for the provided group_id
        group = get_object_or_404(Group, id=group_id)
        # Filter Person objects by the group
        queryset = Person.objects.filter(group=group, is_teacher=False)
        return queryset


class AddGradeView(CreateAPIView):
    serializer_class = PersonModelSerializer

    def create(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        score = request.data.get('score')

        # Fetch the student
        student = get_object_or_404(Person, id=student_id)

        # Update the student's grade
        student.score = score
        student.save()

        serializer = self.get_serializer(student)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateGradeView(UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer

    def update(self, request, *args, **kwargs):
        student_id = self.kwargs.get('pk')
        student = get_object_or_404(Person, id=student_id)

        serializer = self.get_serializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonAPIView(APIView):

    def get(self, request, person_id):
        person = get_object_or_404(Person, id=person_id)
        serializer = PersonModelSerializer(instance=person)
        return Response(serializer.data)
