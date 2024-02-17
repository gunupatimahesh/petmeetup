from django.contrib import admin
from django.urls import path
from petmeetup_app.views import pet_meetup_list, pet_meetup_list_view, \
    dashboard_view, pet_details, api_post_handler

urlpatterns = [
    path('pet_meetup_list/', pet_meetup_list, name='pet_meetup_list'),
    path('pet_meetup_list_veiw/', pet_meetup_list_view, name='pet_meetup_list_view'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('pet_details/<int:pet_id>/', pet_details, name='pet_details'),
    path('api/post/', api_post_handler, name='api_post_handler'),

]