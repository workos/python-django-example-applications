from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import os
# Import views module to ensure workos is loaded before patching
from sso import views


class SSOViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Set environment variables for testing
        os.environ["WORKOS_API_KEY"] = "test_api_key"
        os.environ["WORKOS_CLIENT_ID"] = "test_client_id"
        os.environ["REDIRECT_URI"] = "http://localhost:8000/auth/callback"

    def tearDown(self):
        # Clean up environment variables
        if "WORKOS_API_KEY" in os.environ:
            del os.environ["WORKOS_API_KEY"]
        if "WORKOS_CLIENT_ID" in os.environ:
            del os.environ["WORKOS_CLIENT_ID"]
        if "REDIRECT_URI" in os.environ:
            del os.environ["REDIRECT_URI"]

    def test_login_no_session(self):
        """Test login view when no session is active"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/login.html")

    def test_login_with_active_session(self):
        """Test login view when session is active"""
        session = self.client.session
        session["session_active"] = True
        session["p_profile"] = {"profile": {"first_name": "Test"}}
        session["first_name"] = "Test"
        session["raw_profile"] = {"email": "test@example.com"}
        session.save()

        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/login_successful.html")
        self.assertIn("p_profile", response.context)
        self.assertIn("first_name", response.context)
        self.assertIn("raw_profile", response.context)

    def test_auth_saml_login(self):
        """Test auth view for SAML login"""
        # Create a mock sso object
        mock_sso = MagicMock()
        mock_sso.get_authorization_url.return_value = "https://api.workos.com/sso/authorize?test=123"
        
        # Create a mock client with sso attribute
        mock_client = MagicMock()
        mock_client.sso = mock_sso
        
        with patch.object(views, "workos_client", mock_client):
            response = self.client.post(
                reverse("auth"),
                {"login_method": "saml"},
                follow=False
            )

            # Verify get_authorization_url was called with correct params
            mock_sso.get_authorization_url.assert_called_once()
            call_args = mock_sso.get_authorization_url.call_args
            self.assertIn("redirect_uri", call_args.kwargs)
            self.assertIn("state", call_args.kwargs)
            self.assertIn("organization_id", call_args.kwargs)
            self.assertEqual(call_args.kwargs["organization_id"], views.CUSTOMER_ORGANIZATION_ID)
            self.assertNotIn("provider", call_args.kwargs)

            # Verify redirect response
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "https://api.workos.com/sso/authorize?test=123")

    def test_auth_provider_login(self):
        """Test auth view for provider-based login (Google, Microsoft, etc.)"""
        # Create a mock sso object
        mock_sso = MagicMock()
        mock_sso.get_authorization_url.return_value = "https://api.workos.com/sso/authorize?provider=google"
        
        # Create a mock client with sso attribute
        mock_client = MagicMock()
        mock_client.sso = mock_sso
        
        with patch.object(views, "workos_client", mock_client):
            response = self.client.post(
                reverse("auth"),
                {"login_method": "google"},
                follow=False
            )

            # Verify get_authorization_url was called with correct params
            mock_sso.get_authorization_url.assert_called_once()
            call_args = mock_sso.get_authorization_url.call_args
            self.assertIn("redirect_uri", call_args.kwargs)
            self.assertIn("state", call_args.kwargs)
            self.assertIn("provider", call_args.kwargs)
            self.assertEqual(call_args.kwargs["provider"], "google")
            self.assertNotIn("organization_id", call_args.kwargs)

            # Verify redirect response
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "https://api.workos.com/sso/authorize?provider=google")

    def test_auth_callback_success(self):
        """Test auth_callback view with valid code"""
        # Mock the profile response - in SDK v5+, ProfileAndToken uses .dict() method
        mock_profile = MagicMock()
        mock_profile.dict.return_value = {
            "profile": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            },
            "access_token": "test_token"
        }
        
        # Create a mock sso object
        mock_sso = MagicMock()
        mock_sso.get_profile_and_token.return_value = mock_profile
        
        # Create a mock client with sso attribute
        mock_client = MagicMock()
        mock_client.sso = mock_sso
        
        with patch.object(views, "workos_client", mock_client):
            response = self.client.get(
                reverse("auth_callback"),
                {"code": "test_auth_code"},
                follow=True
            )

            # Verify get_profile_and_token was called with the code
            mock_sso.get_profile_and_token.assert_called_once_with("test_auth_code")

            # Verify session data was set
            self.assertTrue(self.client.session.get("session_active"))
            self.assertIn("p_profile", self.client.session)
            self.assertEqual(self.client.session["first_name"], "John")
            self.assertIn("raw_profile", self.client.session)

            # Verify redirect to login
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "sso/login_successful.html")

    def test_auth_callback_missing_code(self):
        """Test auth_callback view when code parameter is missing"""
        # Create a mock sso object
        mock_sso = MagicMock()
        
        # Create a mock client with sso attribute
        mock_client = MagicMock()
        mock_client.sso = mock_sso
        
        # This should render login page with error message (not raise KeyError)
        with patch.object(views, "workos_client", mock_client):
            response = self.client.get(reverse("auth_callback"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "sso/login.html")
            self.assertIn("error", response.context)
            self.assertEqual(response.context["error"], "missing_code")

    def test_logout(self):
        """Test logout view clears session and redirects"""
        # Set up a session first
        session = self.client.session
        session["session_active"] = True
        session["p_profile"] = {"profile": {"first_name": "Test"}}
        session.save()

        # Verify session has data
        self.assertTrue(self.client.session.get("session_active"))

        # Call logout
        response = self.client.get(reverse("logout"), follow=True)

        # Verify session is cleared
        self.assertFalse(self.client.session.get("session_active"))
        self.assertNotIn("p_profile", self.client.session)

        # Verify redirect to login
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/login.html")
