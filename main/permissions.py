from rest_framework.permissions import BasePermission
from main.models import Membership

class IsOwnerMember(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user:
            return True
        if obj.project.creator == request.user:
            return True
        if Membership.objects.filter(member=request.user, board=obj).exists():
            return True
        # for column
        if Membership.objects.filter(member=request.user, board=obj.board).exists():
            return True
        # for card
        if Membership.objects.filter(member=request.user, board=obj.column.board).exists():
            return True
        if Membership.objects.filter(member=request.user, board=obj.card.column.board).exists():
            return True
        return False