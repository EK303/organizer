from django.urls import path, include

from main.views.projects import ProjectMainView, ProjectDetailView
from main.views.boards import BoardMainView, BoardArchiveView, BoardFavourView

urlpatterns = [
    path("projects/", ProjectMainView.as_view(), name="projects_main"),
    path("project/<int:project_id>/", ProjectDetailView.as_view(), name="project_details"),
    path("project/<int:project_id>/boards", BoardMainView.as_view(), name="boards_main"),
    path("project/<int:project_id>/boards/archive/", BoardArchiveView.as_view(), name="boards_archive"),
    path("project/<int:project_id>/boards/favour/", BoardFavourView.as_view(), name="boards_favour"),
]