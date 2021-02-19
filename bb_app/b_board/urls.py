from django.urls import path

from b_board.views import (
    ad_details,
    ad_create,
    ad_creation,
    ad_statistic,
    add_comment,
    add_tag,
    bb_list,
    success
)


app_name = 'b_board'

urlpatterns = [
    path('list/', bb_list, name='bb_list'),
    path('list/ad/creation/', ad_creation, name='ad_creation'),
    path('list/ad/creation/create', ad_create, name='ad_create'),
    path('list/ad/', ad_details, name='ad_details'),
    path('list/ad/comment', add_comment, name='add_comment'),
    path('list/ad/statistic', ad_statistic, name='ad_statistic'),
    path('list/ad/tag', add_tag, name='add_tag'),
    path('success/', success, name='success'),
]