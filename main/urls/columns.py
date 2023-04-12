from django.urls import path

from main.views.columns import ColumnDetailView
from main.views.cards import CardMainView


urlpatterns = [
    path("column/<int:column_id>", ColumnDetailView.as_view(), name="column_detail"),
    path("column/<int:column_id>/cards", CardMainView.as_view(), name="card_main"),
]