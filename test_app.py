import unittest
import io
from app import app

class TestATSAnalyzer(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data.lower())

    def test_missing_resume(self):
        response = self.client.post('/analyze_resume', data={'job_description': 'developer'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No resume uploaded', response.data)

    def test_successful_resume_analysis(self):
        with open("uploaded_resumes/Darshan_Pandey_Resume_FIXED.pdf", "rb") as f:
            resume = (f, "Darshan_Pandey_Resume_FIXED.pdf")
            job_description = "Looking for a developer who can design systems and lead teams to improve efficiency."

            data = {
                'resume': resume,
                'job_description': job_description
            }

            response = self.client.post('/analyze_resume', data=data, content_type='multipart/form-data')

            print("Response status:", response.status_code)
            print("Response data:", response.data.decode())

            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
