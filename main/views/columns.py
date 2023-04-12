from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from main.models import Column, Board

from main.serializers.columns import ColumnSerializer, ColumnCreateSerializer, ColumnEditSerializer
from main.permissions import IsOwnerMember

class ColumnsMainView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    def get(self, request, board_id):
        board = get_object_or_404(Board, pk=board_id)
        serializer = ColumnSerializer(board.columns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ColumnCreateSerializer)
    def post(self, request, board_id):
        serializer = ColumnCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(f"Column {serializer.data['title']} has been created", status=status.HTTP_201_CREATED)


class ColumnDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]
    def get(self, request, column_id):
        column = get_object_or_404(Column, pk=column_id)
        serializer = ColumnSerializer(column)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ColumnEditSerializer)
    def put(self, request, column_id):
        column = get_object_or_404(Column, pk=column_id)
        serializer = ColumnEditSerializer(column, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(f"Column {serializer.data['title']} has been updated", status=status.HTTP_200_OK)

    def delete(self, request, column_id):
        column = get_object_or_404(Column, pk=column_id)
        column.delete()
        return Response("Column deleted", status=status.HTTP_204_NO_CONTENT)