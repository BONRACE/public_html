from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class PortfolioTests(TestCase):
    def test_index_affiche_les_sections(self):
        r = self.client.get(reverse("portfolio:index"))
        self.assertEqual(r.status_code, 200)
        for texte in ("KPANGON Olivier", "PNUSS", "Les Béatitudes", "UCP", "Tori-Bossito"):
            self.assertContains(r, texte)

    def test_contact_valide_enregistre_le_message(self):
        r = self.client.post(reverse("portfolio:index"), {
            "nom": "Jean", "email": "jean@example.com", "sujet": "Bonjour", "message": "Test",
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_invalide_ne_enregistre_pas(self):
        r = self.client.post(reverse("portfolio:index"), {"nom": "", "email": "x", "sujet": "", "message": ""})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
