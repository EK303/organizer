from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from users.models import TrelloUser
from main.models import Project, Board, Membership, Favourite
from main.serializers.boards import BoardCreateSerializer, BoardListSerializer, BoardArchiveSerializer, \
    BoardEditSerializer, BoardAddMembersSerializer, BoardFavourSerializer, BoardFavourListSerializer
from main.permissions import IsOwnerMember


class BoardMainView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        queryset = project.boards.filter(archived=False)
        serializer = BoardListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardCreateSerializer)
    def post(self, request, project_id):
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    def get(self, request, **kwargs):
        queryset = get_object_or_404(Board, pk=kwargs["board_id"])
        serializer = BoardListSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardEditSerializer)
    def put(self, request, **kwargs):
        queryset = get_object_or_404(Board, pk=kwargs['board_id'])
        serializer = BoardEditSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        board = get_object_or_404(Board, pk=kwargs["board_id"])
        name = board.title
        board.delete()
        return Response(f"{name} has been deleted", status=status.HTTP_204_NO_CONTENT)


class BoardAddMembersView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    @swagger_auto_schema(request_body=BoardAddMembersSerializer)
    def post(self, request, **kwargs):
        board = get_object_or_404(Board, pk=kwargs['board_id'])
        serializer = BoardAddMembersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            for person in serializer.data['members']:
                user = TrelloUser.objects.get(username=person)
                Membership.objects.create(board_id=board.id, member_id=user.id)
            return Response("Member(s) added", status=status.HTTP_201_CREATED)


class BoardArchiveView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        queryset = project.boards.filter(archived=True)
        serializer = BoardListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardArchiveSerializer)
    def post(self, request, **kwargs):
        queryset = get_object_or_404(Board, title=request.data['title'], project_id=kwargs['project_id'])
        serializer = BoardArchiveSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            queryset.archived = request.data['archived']
            queryset.save()
            return Response(f"The {queryset.title} is archived/unarchived", status=status.HTTP_200_OK)


class BoardFavourView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerMember]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        board_in_project = project.boards.values_list('id', flat=True)
        queryset = Favourite.objects.filter(person_id=request.user.id, board_id__in=board_in_project)
        serializer = BoardFavourListSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardFavourSerializer)
    def post(self, request, **kwargs):
        queryset = get_object_or_404(Board, pk=request.data['id'], project_id=kwargs['project_id'])
        favoured_board = Favourite(board_id=request.data['id'], person_id=request.user.id)
        favoured_board.save()
        return Response(f"The {queryset.title} is favoured", status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BoardFavourSerializer)
    def delete(self, request, **kwargs):
        favoured_board = get_object_or_404(Favourite, board_id=request.data['id'], person_id=request.user.id)
        favoured_board_id = favoured_board.id
        favoured_board.delete()
        return Response(f"{favoured_board_id} has been unfavoured", status=status.HTTP_204_NO_CONTENT)
