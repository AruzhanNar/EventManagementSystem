import os
import openpyxl
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from io import BytesIO
from django.test.runner import DiscoverRunner

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create a new Excel workbook and sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = 'Test Results'
sheet.append(['Test Name', 'Status', 'Message'])  # Add headers to the sheet

# Helper function to save test results into the Excel file
def save_test_result(test_name, status, message=""):
    sheet.append([test_name, status, message])

# Sign-in test case
class SigninTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_signin_success(self):
        try:
            response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'password123'})
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('home'))
            save_test_result('Signin Success', 'PASSED')
            print("Test 'signin_success': PASSED")
        except Exception as e:
            save_test_result('Signin Success', 'FAILED', str(e))

    def test_signin_invalid(self):
        try:
            response = self.client.post(reverse('signin'), {'username': 'wronguser', 'password': 'wrongpassword'})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Invalid email or password")
            save_test_result('Signin Invalid', 'PASSED')
            print("Test 'signin_invalid': PASSED")
        except Exception as e:
            save_test_result('Signin Invalid', 'FAILED', str(e))


# Sign-up test case
class SignupTestCase(TestCase):
    def test_signup_success(self):
        try:
            response = self.client.post(reverse('signup'), {
                'username': 'newuser',
                'first_name': 'John',  # Adding mandatory fields
                'last_name': 'Doe',    # Adding mandatory fields
                'email': 'john.doe@example.com',  # Adding email
                'password1': 'Testing_2024',
                'password2': 'Testing_2024',
            })
            self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful registration
            self.assertRedirects(response, reverse('home'))
            save_test_result('Signup Success', 'PASSED')
            print("Test 'signup_success': PASSED")
        except Exception as e:
            save_test_result('Signup Success', 'FAILED', str(e))

    def test_signup_password_mismatch(self):
        try:
            response = self.client.post(reverse('signup'), {
                'username': 'newuser',
                'password1': 'password123',
                'password2': 'wrongpassword',
            })
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "The two password fields didn’t match.")
            save_test_result('Signup Password Mismatch', 'PASSED')
            print("Test 'signup_password_mismatch': PASSED")
        except Exception as e:
            save_test_result('Signup Password Mismatch', 'FAILED', str(e))


# Logout test case
class LogoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_logout(self):
        try:
            response = self.client.get(reverse('logout'))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('home'))
            save_test_result('Logout', 'PASSED')
            print("Test 'logout': PASSED")
        except Exception as e:
            save_test_result('Logout', 'FAILED', str(e))


# Excel report generation test case
class ExcelReportTestCase(TestCase):
    def test_generate_report(self):
        try:
            response = self.client.get(reverse('generate_report'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            excel_file = BytesIO(response.content)
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active

            self.assertEqual(ws['A1'].value, 'ID')
            self.assertEqual(ws['B1'].value, 'Name')
            self.assertEqual(ws['A2'].value, 1)
            self.assertEqual(ws['B2'].value, 'John Doe')
            save_test_result('Generate Excel Report', 'PASSED')
            print("Test 'generate_report': PASSED")
        except Exception as e:
            save_test_result('Generate Excel Report', 'FAILED', str(e))

# Save the test results to an Excel file on the Desktop after running all tests
def save_results_to_excel():
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Get the path to the desktop
    file_path = os.path.join(desktop_path, 'test_results.xlsx')  # Full path to save the file on the desktop
    workbook.save(file_path)
    print(f"Test results saved to: {file_path}")

# Hook to save results after running all tests
class MyTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, **kwargs):  # extra_tests should be removed
        # Call the parent class's run_tests method correctly
        result = super().run_tests(test_labels, **kwargs)
        save_results_to_excel()  # Save to Excel after tests are run
        return result
