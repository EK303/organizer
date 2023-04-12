from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from main.models import Column, Card, Comment

from main.serializers.cards import CardListSerializer, CardCreateSerializer, CardEditSerializer, CommentCreateSerializer
from main.permissions import IsOwnerMember

class CardMainView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    def get(self, request, column_id):
        column = get_object_or_404(Column, pk=column_id)
        serializer = CardListSerializer(column.cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CardCreateSerializer)
    def post(self, request, column_id):
        serializer = CardCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(f"Card {serializer.data['title']} has been created", status=status.HTTP_201_CREATED)


class CardDetailView(APIView):

    def get(self, request, card_id):
        card = get_object_or_404(Card, pk=card_id)
        serializer = CardListSerializer(card)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CardEditSerializer)
    def put(self, request, card_id):
        card = get_object_or_404(Card, pk=card_id)
        serializer = CardEditSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, card_id):
        card = get_object_or_404(Card, pk=card_id)
        card.delete()
        return Response("Card deleted", status=status.HTTP_204_NO_CONTENT)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=CommentCreateSerializer)
    def post(self, request, **kwargs):
        card = get_object_or_404(Card, pk=kwargs['card_id'])
        body = request.data['body']
        comment = Comment(body=body, author=request.user, card=card)
        comment.save()
        return Response(CommentCreateSerializer(comment).data, status=status.HTTP_201_CREATED)