import csv, unittest
from pathlib import Path

class TestComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (Path(__file__).parents[1]/"data/comparative/cyrillic_comparison.csv").open(encoding="utf-8") as f: cls.rows=list(csv.DictReader(f))
    def row(self,ipa): return next(x for x in self.rows if x["ipa"]==ipa)
    def test_russian_aspiration_vs_ukrainian(self):
        r=self.row("kʰ"); self.assertEqual(r["russian_practical"],"кх"); self.assertEqual(r["ukrainian_proposed"],"к")
    def test_h(self):
        r=self.row("h"); self.assertEqual(r["russian_practical"],"х"); self.assertEqual(r["ukrainian_proposed"],"г")
    def test_y(self):
        r=self.row("ɯ"); self.assertEqual(r["russian_practical"],"ы"); self.assertEqual(r["ukrainian_proposed"],"и")
    def test_affricate(self):
        self.assertEqual(self.row("tɕ")["ukrainian_proposed"],"ч")
