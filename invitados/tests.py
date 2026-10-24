from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from eventos.models import Evento

from .models import Invitado


class InvitadoModelTests(TestCase):
    def setUp(self):
        self.e1 = Evento.objects.create(nombre='A', fecha=timezone.now(), lugar='X')
        self.e2 = Evento.objects.create(nombre='B', fecha=timezone.now(), lugar='Y')

    def test_misma_cedula_en_eventos_distintos(self):
        Invitado.objects.create(nombre='Ana', cedula='123456', evento=self.e1)
        Invitado.objects.create(nombre='Ana', cedula='123456', evento=self.e2)
        self.assertEqual(Invitado.objects.filter(cedula='123456').count(), 2)

    def test_cedula_no_se_repite_en_el_mismo_evento(self):
        Invitado.objects.create(nombre='Ana', cedula='123456', evento=self.e1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Invitado.objects.create(nombre='Luis', cedula='123456', evento=self.e1)
