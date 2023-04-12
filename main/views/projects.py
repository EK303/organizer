from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, exceptions

from drf_yasg.utils import swagger_auto_schema

from main.serializers.projects import ProjectListSerializer, ProjectCreateSerializer, ProjectViewSerializer, \
    ProjectEditSerializer
from main.models import Project

from main.permissions import IsOwnerMember


class ProjectMainView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProjectCreateSerializer)
    def post(self, request):
        request.data['creator_username'] = request.user.username
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    def get(self, request, project_id):
        queryset = get_object_or_404(Project, pk=project_id)
        serializer = ProjectViewSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProjectEditSerializer)
    def put(self, request, project_id):
        queryset = get_object_or_404(Project, pk=project_id)
        serializer = ProjectEditSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_id):
        queryset = get_object_or_404(Project, pk=project_id)
        queryset.delete()
        return Response(f"Project has been deleted", status=status.HTTP_204_NO_CONTENT)
