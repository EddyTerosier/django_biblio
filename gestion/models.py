from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Livre(models.Model):
    theme = models.CharField(max_length=120)
    auteur = models.CharField(max_length=120)
    titre = models.CharField(max_length=200)
    note = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titre} — {self.auteur} ({'dispo' if self.disponibilite else 'indispo'})"


class Personne(models.Model):
    nom = models.CharField(max_length=120)
    prenom = models.CharField(max_length=120)
    age = models.PositiveIntegerField()
    lieu_residence = models.CharField(max_length=120)
    livre_emprunte = models.OneToOneField(
        Livre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emprunteur"
    )

    def clean(self):
        if self.age < 18:
            raise ValidationError("Les mineurs ne peuvent pas emprunter de livre.")
        if self.lieu_residence.lower() != "montreuil":
            raise ValidationError("Seules les personnes résidant à Montreuil peuvent emprunter un livre.")
        if self.livre_emprunte and not self.livre_emprunte.disponibilite:
            raise ValidationError(f"Le livre '{self.livre_emprunte.titre}' est déjà indisponible.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        if self.livre_emprunte and self.livre_emprunte.disponibilite:
            self.livre_emprunte.disponibilite = False
            self.livre_emprunte.save()

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.lieu_residence}"