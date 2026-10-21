from django.db import models


class ContactMessage(models.Model):
    """Message envoyé via le formulaire de contact."""
    nom = models.CharField("Nom", max_length=120)
    email = models.EmailField("Email")
    sujet = models.CharField("Sujet", max_length=200)
    message = models.TextField("Message")
    cree_le = models.DateTimeField("Reçu le", auto_now_add=True)
    lu = models.BooleanField("Lu", default=False)

    class Meta:
        ordering = ["-cree_le"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.nom} — {self.sujet}"


class Experience(models.Model):
    """Étape du parcours professionnel (modifiable depuis l'admin)."""
    THEMES = [("sante", "Gouvernance sanitaire"), ("agro", "Agro-sylvo-pastoral")]

    ancre = models.SlugField("Ancre (id HTML)", unique=True)
    theme = models.CharField("Thème de couleur", max_length=10, choices=THEMES)
    titre = models.CharField("Titre", max_length=150)
    role = models.CharField("Rôle", max_length=200)
    localite = models.CharField("Localité", max_length=120, blank=True)
    icone = models.CharField("Icône Lucide", max_length=40, default="briefcase")
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["ordre"]
        verbose_name = "Expérience"

    def __str__(self):
        return self.titre


class Mission(models.Model):
    experience = models.ForeignKey(Experience, related_name="missions", on_delete=models.CASCADE)
    intitule = models.CharField("Intitulé", max_length=150)
    description = models.TextField("Description")
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["ordre"]

    def __str__(self):
        return self.intitule


class Competence(models.Model):
    titre = models.CharField("Titre", max_length=150)
    description = models.TextField("Description")
    icone = models.CharField("Icône Lucide", max_length=40, default="award")
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["ordre"]

    def __str__(self):
        return self.titre
