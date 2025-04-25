from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ClientSignupView, VerifyEmailView, OpsFileUploadView, FileListView, GenerateDownloadLinkView, SecureDownloadView

urlpatterns = [
    # We'll add routes here as we go
    path('signup/', ClientSignupView.as_view(), name='signup'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', OpsFileUploadView.as_view(), name='upload-file'),
    path('files/', FileListView.as_view(), name='list-files'),
    path('download-link/<int:pk>/', GenerateDownloadLinkView.as_view(), name='generate-download-link'),
    path('download-file/', SecureDownloadView.as_view(), name='download-file'),
]
