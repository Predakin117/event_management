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


class CrearInvitadoViewTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse
        self.reverse = reverse
        get_user_model().objects.create_user('ana', password='clave-segura-123')
        self.evento = Evento.objects.create(nombre='A', fecha=timezone.now(), lugar='X')
        self.url = reverse('invitados:crear')

    def test_requiere_sesion(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_crea_invitado(self):
        self.client.login(username='ana', password='clave-segura-123')
        r = self.client.post(self.url, {'nombre': 'Luis', 'cedula': '1020304050', 'evento': self.evento.pk})
        self.assertRedirects(r, self.reverse('eventos:detalle', args=[self.evento.pk]))
        self.assertTrue(Invitado.objects.filter(cedula='1020304050').exists())

    def test_cedula_duplicada_en_el_evento_muestra_error(self):
        self.client.login(username='ana', password='clave-segura-123')
        Invitado.objects.create(nombre='Luis', cedula='1020304050', evento=self.evento)
        r = self.client.post(self.url, {'nombre': 'Otro', 'cedula': '1020304050', 'evento': self.evento.pk})
        self.assertContains(r, 'ya está invitada')

    def test_cedula_con_letras_es_invalida(self):
        self.client.login(username='ana', password='clave-segura-123')
        r = self.client.post(self.url, {'nombre': 'Luis', 'cedula': 'abc', 'evento': self.evento.pk})
        self.assertContains(r, 'Escribe solo números')
