from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.

class FileSharingTests(APITestCase):

    def setUp(self):
        self.ops_user = User.objects.create_user(username="ops", password="test1234", role="OPS", email="ops@example.com")
        self.client_user = User.objects.create_user(username="client", password="test1234", role="CLIENT", email="client@example.com", is_email_verified=True)

        self.ops_token = RefreshToken.for_user(self.ops_user).access_token
        self.client_token = RefreshToken.for_user(self.client_user).access_token

        self.file = SimpleUploadedFile("test.docx", b"file_content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    def test_ops_file_upload(self):
        url = reverse("upload-file")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.ops_token}')
        response = self.client.post(url, {'file': self.file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_upload_file(self):
        url = reverse("upload-file")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        response = self.client.post(url, {'file': self.file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_files_as_client(self):
        # upload a file first
        File.objects.create(uploaded_by=self.ops_user, file=self.file)
        url = reverse("list-files")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_generate_download_link_as_client(self):
        file = File.objects.create(uploaded_by=self.ops_user, file=self.file)
        url = reverse("generate-download-link", args=[file.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("download-link", response.data)

    def test_download_file_with_valid_token(self):
        file = File.objects.create(uploaded_by=self.ops_user, file=self.file)
        from .utils import generate_file_token
        token = generate_file_token(file.id)
        url = reverse("download-file") + f"?token={token}"
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
