from unittest import TestCase

from questionnaire.validators import validate_gender


class ValidatorsTestCase(TestCase):

    def test_validate_gender_not_int(self):
        r = validate_gender('random')
        self.assertIsNone(r)
