from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Board, Mark

from main.serializers.marks import MarkCreateSerializer, MarkListSerializer

from drf_yasg.utils import swagger_auto_schema

from main.permissions import IsOwnerMember


class MarkCreateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    @swagger_auto_schema(request_body=MarkCreateSerializer)
    def post(self, request, **kwargs):
        board = get_object_or_404(Board, pk=kwargs["board_id"])
        serializer = MarkCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MarkDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, **kwargs):
        mark = get_object_or_404(Mark, pk=kwargs["mark_id"])
        serializer = MarkListSerializer(mark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MarkCreateSerializer)
    def put(self, request, **kwargs):
        mark = get_object_or_404(Mark, pk=kwargs["mark_id"])
        serializer = MarkCreateSerializer(mark, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(f"Mark {request.data['title']} has been updated", status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        mark = get_object_or_404(Mark, pk=kwargs["mark_id"])
        mark.delete()
        return Response("Mark has been deleted", status=status.HTTP_204_NO_CONTENT)