from django.urls import path

from main.views.boards import BoardDetailView, BoardAddMembersView
from main.views.columns import ColumnsMainView
from main.views.marks import MarkCreateView

urlpatterns = [
    path("board/<int:board_id>", BoardDetailView.as_view(), name="board_detail"),
    path("board/<int:board_id>/members", BoardAddMembersView.as_view(), name="board_members"),
    path("board/<int:board_id>/columns", ColumnsMainView.as_view(), name="column_main"),
    path("board/<int:board_id>/marks", MarkCreateView.as_view(), name="marks_main"),
]