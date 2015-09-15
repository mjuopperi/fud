from django.test import TestCase

# Example test
class ExampleTestCase(TestCase):
    # tests need to start with test<name>
    def test_true_is_true(self):
        """Testing that true asserts as true"""
        self.assertEqual(True, True)
