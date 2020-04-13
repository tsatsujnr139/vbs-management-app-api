from django.urls import path, include

from participant import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('grades', views.GradeViewSet)
router.register('churches', views.ChurchViewSet)
router.register('participants', views.ParticipantViewset,
                basename='participant')
router.register('volunteers', views.VolunteerViewSet)

app_name = 'participant'

urlpatterns = [
    path('', include(router.urls))
]
