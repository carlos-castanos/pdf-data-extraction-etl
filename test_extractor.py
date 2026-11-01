import unittest

from extractor import get_latest_participation, get_record_type, is_checked


class FakeField:
    def __init__(self, value):
        self.value = value


class ExtractorTests(unittest.TestCase):
    def test_is_checked_accepts_pdf_checkbox_value(self):
        self.assertTrue(is_checked("/Yes"))
        self.assertFalse(is_checked("/Off"))

    def test_latest_checked_month_wins(self):
        fields = {
            "901_20_CheckBox": FakeField("/Yes"),
            "902_20_Text_C_SanSerif": FakeField("1"),
            "903_20_CheckBox": FakeField("/Off"),
            "904_20_S21_Value": FakeField("10"),
            "901_21_CheckBox": FakeField("/Yes"),
            "902_21_Text_C_SanSerif": FakeField("2"),
            "903_21_CheckBox": FakeField("/Yes"),
            "904_21_S21_Value": FakeField("12"),
        }

        result = get_latest_participation(fields)

        self.assertEqual(result["Mes"], "Octubre")
        self.assertEqual(result["Cursos"], "2")
        self.assertEqual(result["Horas"], "12")
        self.assertTrue(result["Auxiliar"])

    def test_no_participation_returns_empty_month(self):
        result = get_latest_participation({})
        self.assertIsNone(result["Mes"])
        self.assertFalse(result["Auxiliar"])

    def test_record_type_classification(self):
        self.assertEqual(get_record_type({}, auxiliary=True), "AUX")
        self.assertEqual(
            get_record_type({"900_10_CheckBox": FakeField("/Yes")}, auxiliary=False),
            "REG",
        )
        self.assertEqual(get_record_type({}, auxiliary=False), "PUB")


if __name__ == "__main__":
    unittest.main()
