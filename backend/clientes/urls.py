from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoDocumentoViewSet,
    ClienteViewSet,
    ReporteFidelizacionViewSet
)

router = DefaultRouter()
router.register(r'tipos-documento', TipoDocumentoViewSet, basename='tipos-documento')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'reporte-fidelizacion', ReporteFidelizacionViewSet, basename='reporte-fidelizacion')

urlpatterns = [
    path('', include(router.urls)),
]

