import unittest
from datetime import datetime, timedelta
from main import round_time, calculate_work_hours, veri_cache

class TestCalismaSuresi(unittest.TestCase):

    def test_round_time(self):
        self.assertEqual(round_time(datetime(2024, 1, 1, 8, 0)), datetime(2024, 1, 1, 8, 0))
        self.assertEqual(round_time(datetime(2024, 1, 1, 8, 7)), datetime(2024, 1, 1, 8, 0))
        self.assertEqual(round_time(datetime(2024, 1, 1, 8, 10)), datetime(2024, 1, 1, 8, 15))
        self.assertEqual(round_time(datetime(2024, 1, 1, 8, 30)), datetime(2024, 1, 1, 8, 30))
        self.assertEqual(round_time(datetime(2024, 1, 1, 8, 59)), datetime(2024, 1, 1, 9, 0))

    def test_calculate_work_hours_weekday(self):
        sonuc = calculate_work_hours("08:00", "17:00", True)
        self.assertAlmostEqual(sonuc, 8.25)  # 9 saat - 0.75 saat (öğle ve akşam molası)

    def test_calculate_work_hours_weekend(self):
        sonuc = calculate_work_hours("10:00", "20:00", False)
        self.assertAlmostEqual(sonuc, 9.0)  # 10 saat - 1 saat (2x30dk mola)

    def test_veri_cache_update(self):
        calculate_work_hours("09:00", "18:00", True)
        self.assertIsNotNone(veri_cache["entry"])
        self.assertIsNotNone(veri_cache["exit"])
        self.assertIsNotNone(veri_cache["net_duration"])
        self.assertEqual(veri_cache["entry"].minute % 15, 0)
        self.assertEqual(veri_cache["exit"].minute % 15, 0)

if __name__ == '__main__':
    unittest.main()
