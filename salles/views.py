"""Taches 3, 4, 5 (et bonus) : vues de l'API.

A FAIRE :
  - SalleViewSet (ModelViewSet), avec l'action `occupation` (tache 5)
  - ReservationViewSet (ModelViewSet), avec perform_create (tache 3)
"""
from rest_framework import viewsets  # noqa: F401  (a utiliser)

from .models import Reservation, Salle  # noqa: F401  (a utiliser)
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ReservationSerializer, SalleSerializer  # noqa: F401  (a utiliser)
# TODO : votre code ici
# t3
class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer

    # t5
    @action(detail=True, methods=["get"])
    def occupation(self, request, pk=None):
          salle = self.get_object()
          debut = parse_datetime(request.query_params.get("debut", ""))
          fin = parse_datetime(request.query_params.get("fin", ""))
    
          if debut is None or fin is None or fin <= debut:
              return Response({"erreur": "Les paramètres ne sont pas valides"}, status=400)
    
          
          reservations = salle.reservations.filter(statut=Reservation.Statut.CONFIRMEE,
              debut__lt=fin,
              fin__gt=debut,
          )
          duree_de_reservation = 0 
          for i in reservations:
              debut_effectif = max(i.debut, debut)
              fin_effective = min(i.fin, fin)
              duree_de_reservation += (fin_effective - debut_effectif).total_seconds()
          duree_totale = (fin - debut).total_seconds()
          return Response({"le taux d'occupation est": duree_de_reservation / duree_totale })
# t3
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)



    