from django.urls import path
from .views import (
    TreatmentListView,
    TreatmentDetailBySlugView,
    TreatmentIntroView,
    TreatmentCategoryListView,
    TreatmentRetrieveView,
    TreatmentsByCategoryView,
    TreatmentDoctorsView,
    TreatmentHospitalsView
   
)

from .views import (
    TreatmentSymptomsView,
    TreatmentPrecautionsView,
    TreatmentRiskFactorsView,
    TreatmentPreparationsView,
    TreatmentProcedureView,
    TreatmentPostProcedureView,
    TreatmentSuccessRateView,
)

urlpatterns = [
    path('api/treatments/', TreatmentListView.as_view(), name='treatment-list'),
    path('api/treatments/<slug:slug>/', TreatmentRetrieveView.as_view(), name='treatments'),
    path('api/treatment-details/<slug:treatment_name>/', TreatmentDetailBySlugView.as_view(), name='treatment-details'),
    path('api/treatment-intro/<slug:slug>/', TreatmentIntroView.as_view(), name='treatment-intro'),
    path('treatment-categories/', TreatmentCategoryListView.as_view(), name='treatment-category-list'),
    path('treatments/category/<str:category_slug>/', TreatmentsByCategoryView.as_view(), name='treatments-by-category'),
    path('treatment/<slug:slug>/doctors/', TreatmentDoctorsView.as_view(), name='treatment-doctors'),
    path('treatment/<slug:slug>/hospitals/', TreatmentHospitalsView.as_view(), name='treatment-hospitals'),
    path('treatments/<slug:slug>/symptoms/', TreatmentSymptomsView.as_view(), name='treatment-symptoms'),
    path('treatments/<slug:slug>/precautions/', TreatmentPrecautionsView.as_view(), name='treatment-precautions'),
    path('treatments/<slug:slug>/risk-factors/', TreatmentRiskFactorsView.as_view(), name='treatment-risk-factors'),
    path('treatments/<slug:slug>/preparations/', TreatmentPreparationsView.as_view(), name='treatment-preparations'),
    path('treatments/<slug:slug>/procedure/', TreatmentProcedureView.as_view(), name='treatment-procedure'),
    path('treatments/<slug:slug>/post-procedure/', TreatmentPostProcedureView.as_view(), name='treatment-post-procedure'),
    path('treatments/<slug:slug>/success-rate/', TreatmentSuccessRateView.as_view(), name='treatment-success-rate'),

    
]
