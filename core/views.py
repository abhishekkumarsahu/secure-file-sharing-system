from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,  generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import FileResponse, Http404
from .models import User, File
from .serializers import ClientSignupSerializer, FileUploadSerializer
from .utils import generate_verification_token, verify_token, generate_file_token, verify_file_token
from django.urls import reverse

# Create your views here.

class ClientSignupView(APIView):
    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # generate token and email link
            token = generate_verification_token(user.email)
            verification_link = request.build_absolute_uri(
                reverse('verify-email') + f"?token={token}"
            )

            # send verification email
            send_mail(
                subject="Verify Your Email",
                message=f"Click to verify: {verification_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response({"message": "User registered. Verification email sent."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        email = verify_token(token)
        if email:
            try:
                user = User.objects.get(email=email)
                user.is_email_verified = True
                user.save()
                return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
    
class OpsFileUploadView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'OPS':
            raise PermissionDenied("Only Ops users can upload files.")
        serializer.save(uploaded_by=self.request.user)

class FileListView(generics.ListAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'CLIENT':
            raise PermissionDenied("Only Client users can view file list.")
        return File.objects.all()

class GenerateDownloadLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if request.user.role != 'CLIENT':
            raise PermissionDenied("Only Client users can request download links.")

        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return Response({"error": "File not found"}, status=404)

        token = generate_file_token(file.id)
        download_url = request.build_absolute_uri(
            reverse('download-file') + f"?token={token}"
        )
        return Response({
            "download-link": download_url,
            "message": "success"
        })
    
class SecureDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.GET.get('token')
        file_id = verify_file_token(token)

        if not file_id:
            return Response({"error": "Invalid or expired link."}, status=400)

        if request.user.role != 'CLIENT':
            raise PermissionDenied("Only Client users can access download links.")

        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            raise Http404("File not found")

        return FileResponse(file.file, as_attachment=True)