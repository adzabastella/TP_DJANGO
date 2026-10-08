"""Tache 1 et 2 : serializers et validation.

A FAIRE :
  - SalleSerializer (ModelSerializer)
  - ReservationSerializer (ModelSerializer) :
      * le champ `utilisateur` est en LECTURE SEULE (il sera renseigne par la vue)
      * validation : `fin` strictement apres `debut`
      * validation : pas de chevauchement avec une autre reservation CONFIRMEE
        de la meme salle
"""
from rest_framework import serializers

from .models import Reservation, Salle  # noqa: F401  (a utiliser)

# t1
class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = ["id", "nom", "capacite","batiment"]
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "salle", "utilisateur", "debut", "fin", "motif", "statut", "cree_le"]
        read_only_fields = ["utilisateur", "cree_le"]
        # t2
    def validate(self, data):
        instance = self.instance
        debut = data.get("debut", instance.debut if instance else None)
        fin = data.get("fin", instance.fin if instance else None)
        salle = data.get("salle", instance.salle if instance else None)
        statut = data.get("statut", instance.statut if instance else Reservation.Statut.CONFIRMEE)
        if debut and fin and fin <= debut:
                raise serializers.ValidationError("La date de fin doit venir après la date de debut.")

        if statut == Reservation.Statut.CONFIRMEE:
            conflit = Reservation.objects.filter(
                salle=salle,
                statut=Reservation.Statut.CONFIRMEE,
                debut__lt=fin,
                fin__gt=debut,
            )
            if instance:
                conflit = conflit.exclude(pk=instance.pk)
            if conflit.exists():
                raise serializers.ValidationError("Cette reservation chevauche une autre reservation confirme de la meme salle.")
        return data
