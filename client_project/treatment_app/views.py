# treatment_app/views.py

from rest_framework import viewsets, generics, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Treatment, TreatmentDetail, TreatmentIntro, TreatmentCategory
from .serializers import (
    TreatmentSerializer,
    TreatmentDetailSerializer,
    TreatmentIntroSerializer,
    TreatmentCategorySerializer,
    
   
)
from django.shortcuts import get_object_or_404

# 1. ViewSet for standard CRUD operations (optional)
class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

# 2. List all treatments
class TreatmentListView(generics.ListAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

# 3. Get treatment detail using slug
class TreatmentDetailBySlugView(RetrieveAPIView):
    serializer_class = TreatmentDetailSerializer

    def get_object(self):
        slug = self.kwargs.get("treatment_name")
        try:
            return TreatmentDetail.objects.select_related('treatment').get(treatment__slug=slug)
        except TreatmentDetail.DoesNotExist:
            raise NotFound("Treatment detail not found for the given slug.")

# 4. Get introduction section (separate model)
class TreatmentIntroView(APIView):
    def get(self, request, slug):
        try:
            treatment = Treatment.objects.get(slug=slug)
            intro = treatment.intro  # related_name from OneToOneField
            serializer = TreatmentIntroSerializer(intro)
            return Response(serializer.data)
        except Treatment.DoesNotExist:
            return Response({'error': 'Treatment not found'}, status=status.HTTP_404_NOT_FOUND)
        except TreatmentIntro.DoesNotExist:
            return Response({'error': 'Intro not available for this treatment'}, status=status.HTTP_404_NOT_FOUND)

class TreatmentCategoryListView(generics.ListAPIView):
    queryset = TreatmentCategory.objects.all()
    serializer_class = TreatmentCategorySerializer

# treatment_app/views.py

class TreatmentsByCategoryView(generics.ListAPIView):
    serializer_class = TreatmentSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        return Treatment.objects.filter(category__slug=category_slug)

class TreatmentDoctorsView(RetrieveAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    lookup_field = 'slug'

class TreatmentHospitalsView(RetrieveAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    lookup_field = 'slug'

class TreatmentRetrieveView(RetrieveAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    lookup_field = 'slug'  # or 'slug' if you prefer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Treatment


class TreatmentSymptomsView(APIView):
    def get(self, request, slug):
        treatment = get_object_or_404(Treatment, slug=slug)
        return Response({'symptoms': treatment.symptoms})


class TreatmentPrecautionsView(APIView):
    def get(self, request, slug):
        treatment = get_object_or_404(Treatment, slug=slug)
        return Response({'faqs': treatment.faqs})


class TreatmentRiskFactorsView(APIView):
    def get(self, request, slug):
        treatment = get_object_or_404(Treatment, slug=slug)
        return Response({'risk_factors': treatment.risk_factors})


class TreatmentPreparationsView(APIView):
    def get(self, request, slug):
        treatment = get_object_or_404(Treatment, slug=slug)
        return Response({'preparations': treatment.preparations})


class TreatmentProcedureView(APIView):
    def get(self, request, slug):
        treatment = get_object_or_404(Treatment, slug=slug)
        return Response({'procedure': treatment.procedure})


class TreatmentPostProcedureView(APIView):
    def get(self, request, slug):
        treatment = get_object_or_404(Treatment, slug=slug)
        return Response({'post_procedure': treatment.post_procedure})


class TreatmentSuccessRateView(APIView):
    def get(self, request, slug):
        treatment = get_object_or_404(Treatment, slug=slug)
        return Response({'success_rate': treatment.success_rate})
