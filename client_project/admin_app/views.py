# admin_app/views.py

import logging
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from webinar_app.models import Webinar, WebinarBooking
from webinar_app.serializers import WebinarBookingSerializer, WebinarSerializer
from treatment_app.models import Treatment, TreatmentCategory, TreatmentDetail, TreatmentIntro
from treatment_app.serializers import TreatmentCategorySerializer, TreatmentDetailSerializer, TreatmentIntroSerializer
from doctor_app.models import Doctor
from doctor_app.serializers import DoctorReviewSerializer, DoctorSerializer
from review_app.models import DoctorReview
from hospital_app.models import Hospital,Specialty,HospitalType
from hospital_review.models import HospitalReview
from hospital_review.serializers import HospitalReviewSerializer
from hospital_app.serializers import HospitalSerializer,AccreditationSerializer, TreatmentSerializer
from hospital_app.serializers import SpecialtySerializer
from hospital_app.serializers import HospitalTypeSerializer
from hospital_app.serializers import AlliedServiceSerializer
from hospital_review.serializers import HospitalAverageRatingSerializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
import traceback
from hospital_app.models import AlliedService  # Add this import
from hospital_app.models import Accreditation  # Add this import
from doctor_app.models import SpecializationIcon  # Add this import
from doctor_app.serializers import SpecializationIconSerializer  # Add this import
from rest_framework.views import APIView
from rest_framework import viewsets



logger = logging.getLogger(__name__)

# Hospital CRUD Views
class HospitalListCreateView(generics.ListCreateAPIView):
    queryset = Hospital.objects.all()  # type: ignore
    serializer_class = HospitalSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        logger.info(f"FILES: {request.FILES}")
        logger.info(f"DATA: {request.data}")

        # --- Custom parsing for nested galleries and awards with files ---
        data = request.data.copy()  # QueryDict
        files = request.FILES

        # Helper to extract nested fields like galleries[0][title], awards[1][image], etc.
        def extract_nested(prefix):
            result = {}
            for key in data:
                if key.startswith(prefix):
                    # e.g. galleries[0][title] -> 0, title
                    import re
                    m = re.match(rf'{prefix}\[(\d+)\]\[(\w+)\]', key)
                    if m:
                        idx, field = int(m.group(1)), m.group(2)
                        if idx not in result:
                            result[idx] = {}
                        result[idx][field] = data[key]
            for key in files:
                if key.startswith(prefix):
                    import re
                    m = re.match(rf'{prefix}\[(\d+)\]\[(\w+)\]', key)
                    if m:
                        idx, field = int(m.group(1)), m.group(2)
                        if idx not in result:
                            result[idx] = {}
                        result[idx][field] = files[key]
            # Convert to list
            return [result[idx] for idx in sorted(result.keys())]

        galleries = extract_nested('galleries')
        awards = extract_nested('awards')
        mutable_data = data.copy()
        mutable_data.setlist('galleries', [])
        mutable_data.setlist('awards', [])
        serializer = self.get_serializer(data={**mutable_data, 'galleries': galleries, 'awards': awards})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class HospitalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()  # type: ignore
    serializer_class = HospitalSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def update(self, request, *args, **kwargs):
        logger.info(f"FILES: {request.FILES}")
        logger.info(f"DATA: {request.data}")
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            
            logger.info(f"Updating hospital {instance.id} - Partial: {partial}")
            logger.info(f"Request data: {request.data}")
            
            # For PUT requests, we need to provide all required fields
            if not partial:
                # Get the current instance data and merge with request data
                current_data = HospitalSerializer(instance).data
                # Remove read-only fields
                for field in ['id', 'created_at', 'updated_at']:
                    current_data.pop(field, None)
                
                # Merge current data with request data
                merged_data = {**current_data, **request.data}
                logger.info(f"Merged data for PUT: {merged_data}")
                serializer = self.get_serializer(instance, data=merged_data, partial=False)
            else:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
            
            # Validate the data
            if not serializer.is_valid():
                logger.error(f"Validation errors: {serializer.errors}")
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            # Perform the update
            updated_instance = serializer.save()
            logger.info(f"Hospital {instance.id} updated successfully")
            
            return Response(serializer.data)
        except IntegrityError as e:
            logger.error(f"Integrity error updating hospital: {e}")
            error_message = str(e)
            
            # Handle specific integrity errors
            if 'slug' in error_message.lower():
                return Response({
                    'error': 'A hospital with this slug already exists. Please choose a different slug or leave it empty to auto-generate.'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif 'name' in error_message.lower():
                return Response({
                    'error': 'A hospital with this name already exists. Please choose a different name.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'Database constraint violation. Please check your data and try again.'
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error updating hospital: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating hospital: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response({'error': 'An error occurred while updating the hospital'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

# Specialty CRUD Views
class SpecialtyListCreateView(generics.ListCreateAPIView):
    queryset = Specialty.objects.all()  # type: ignore
    serializer_class = SpecialtySerializer
    parser_classes = (MultiPartParser, FormParser)

class SpecialtyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()  # type: ignore
    serializer_class = SpecialtySerializer
    parser_classes = (MultiPartParser, FormParser)

# HospitalType CRUD Views
class HospitalTypeListCreateView(generics.ListCreateAPIView):
    queryset = HospitalType.objects.all()  # type: ignore
    serializer_class = HospitalTypeSerializer
    parser_classes = (MultiPartParser, FormParser)

class HospitalTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HospitalType.objects.all()  # type: ignore
    serializer_class = HospitalTypeSerializer
    parser_classes = (MultiPartParser, FormParser)

class AlliedServiceListCreateView(generics.ListCreateAPIView):
    queryset = AlliedService.objects.all()
    serializer_class = AlliedServiceSerializer

class AlliedServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlliedService.objects.all()
    serializer_class = AlliedServiceSerializer

class AccreditationListCreateView(generics.ListCreateAPIView):
    queryset = Accreditation.objects.all()
    serializer_class = AccreditationSerializer

class AccreditationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accreditation.objects.all()
    serializer_class = AccreditationSerializer

from django.shortcuts import get_object_or_404
from django.db.models import Avg  # Add this import for aggregation
# Hospital Review CRUD Views
class HospitalReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = HospitalReviewSerializer

    def get_queryset(self):
        hospital_id = self.request.query_params.get('hospital_id')
        if hospital_id:
            return HospitalReview.objects.filter(hospital_id=hospital_id).order_by('-created_at')
        return HospitalReview.objects.none()

    def perform_create(self, serializer):
        hospital_id = self.request.data.get('hospital_id')
        hospital = get_object_or_404(Hospital, pk=hospital_id)
        serializer.save(hospital=hospital)


class HospitalReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HospitalReviewSerializer

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return HospitalReview.objects.filter(hospital_id=hospital_id).order_by('-created_at')

    def perform_create(self, serializer):
        hospital_id = self.kwargs['hospital_id']
        serializer.save(hospital_id=hospital_id)

class HospitalAverageRatingView(APIView):
    def get(self, request, hospital_id):
        average = HospitalReview.objects.filter(hospital_id=hospital_id, is_active=True).aggregate(avg_rating=Avg('rating'))
        avg_rating = average['avg_rating'] if average['avg_rating'] is not None else 0.0

        serializer = HospitalAverageRatingSerializer(data={'average_rating': round(avg_rating, 1)})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SpecializationIconViewSet(viewsets.ModelViewSet):
    queryset = SpecializationIcon.objects.all()
    serializer_class = SpecializationIconSerializer

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    parser_classes = (MultiPartParser, FormParser)

class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    

class DoctorReviewListCreateView(generics.ListCreateAPIView):
    queryset = DoctorReview.objects.all()
    serializer_class = DoctorReviewSerializer

class DoctorReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorReview.objects.all()
    serializer_class = DoctorReviewSerializer


class TreatmentListCreateView(generics.ListCreateAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

class TreatmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

class TreatmentCategoryListCreateView(generics.ListCreateAPIView):
    queryset = TreatmentCategory.objects.all()
    serializer_class = TreatmentCategorySerializer

class TreatmentCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TreatmentCategory.objects.all()
    serializer_class = TreatmentCategorySerializer

class TreatmentDetailViewSet(viewsets.ModelViewSet):
    queryset = TreatmentDetail.objects.all()
    serializer_class = TreatmentDetailSerializer

class TreatmentDetailRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TreatmentDetail.objects.all()
    serializer_class = TreatmentDetailSerializer

class TreatmentIntroViewSet(viewsets.ModelViewSet):
    queryset = TreatmentIntro.objects.all()
    serializer_class = TreatmentIntroSerializer

class TreatmentIntroRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TreatmentIntro.objects.all()
    serializer_class = TreatmentIntroSerializer

class TreatmentsByCategoryView(generics.ListAPIView):
    serializer_class = TreatmentSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        return Treatment.objects.filter(category__slug=category_slug)

class AdminWebinarListCreateView(generics.ListCreateAPIView):
    queryset = Webinar.objects.all().order_by('-date')
    serializer_class = WebinarSerializer

# 🔹 Retrieve, Update, Delete Webinars
class AdminWebinarRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer

# 🔹 List Webinar Bookings (optional)
class AdminWebinarBookingListView(generics.ListAPIView):
    queryset = WebinarBooking.objects.all().select_related('webinar', 'user')
    serializer_class = WebinarBookingSerializer

class AdminWebinarBookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WebinarBooking.objects.all().select_related('webinar', 'user')
    serializer_class = WebinarBookingSerializer

from django.shortcuts import get_object_or_404, render

class AdminWebinarBookingInvoiceView(generics.GenericAPIView):
    def get(self, request, pk):
        booking = get_object_or_404(WebinarBooking, pk=pk)

        # Optional: add more details like pricing, user, payment info, etc.
        context = {
            'booking': booking,
            'user': booking.user,
            'treatment_title': booking.webinar,  # this is already set as treatment title
            'price': 500,  # fixed price as you wanted
        }

        return render(request, 'admin_panel/invoice_template.html', context)