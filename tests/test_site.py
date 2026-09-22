from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", ROOT / "privacy/index.html", ROOT / "terms/index.html"]


class SiteTest(unittest.TestCase):
    def test_pages_exist(self):
        for page in PAGES:
            self.assertTrue(page.is_file(), str(page))

    def test_navigation(self):
        home = PAGES[0].read_text(encoding="utf-8")
        self.assertIn('href="privacy/"', home)
        self.assertIn('href="terms/"', home)
        for page in PAGES[1:]:
            self.assertIn('href="../"', page.read_text(encoding="utf-8"))

    def test_no_sensitive_text(self):
        forbidden = re.compile(
            r"hhee|tailscale|192\.168\.|100\.99\.|@gmail\.com|"
            r"client_secret|refresh_token|GOCSPX|<script|<form", re.I
        )
        for page in PAGES:
            self.assertIsNone(forbidden.search(page.read_text(encoding="utf-8")))

    def test_not_yet_operational(self):
        home = PAGES[0].read_text(encoding="utf-8").lower()
        self.assertIn("en preparación", home)
        self.assertIn("no confirma que el respaldo automático ya esté activo", home)


if __name__ == "__main__":
    unittest.main()
