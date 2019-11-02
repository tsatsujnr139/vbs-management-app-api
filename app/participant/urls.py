from django.urls import path, include

from participant import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('grades', views.GradeViewSet)
router.register('churches', views.ChurchViewSet)
router.register('pickuppersons', views.PickupPersonViewSet)

app_name = 'participant'

urlpatterns = [
    path('', include(router.urls))
]
