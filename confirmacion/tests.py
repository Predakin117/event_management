from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from eventos.models import Evento
from invitados.models import Invitado

from . import servicios


def crear_datos():
    boda = Evento.objects.create(nombre='Boda', fecha=timezone.now(), lugar='Jardín')
    feria = Evento.objects.create(nombre='Feria Tech', fecha=timezone.now(), lugar='Auditorio')
    Invitado.objects.create(nombre='Ana Pérez', cedula='1020304050', evento=boda)
    Invitado.objects.create(nombre='Ana Pérez', cedula='1020304050', evento=feria)
    return boda, feria


class ServiciosTests(TestCase):
    def setUp(self):
        crear_datos()

    def test_devuelve_todas_las_invitaciones(self):
        invitaciones = servicios.buscar_invitaciones('1020304050')
        self.assertEqual({i.evento.nombre for i in invitaciones}, {'Boda', 'Feria Tech'})

    def test_cedula_inexistente_devuelve_lista_vacia(self):
        self.assertEqual(servicios.buscar_invitaciones('99999999'), [])


class ConfirmarViewTests(TestCase):
    def setUp(self):
        crear_datos()
        self.url = reverse('confirmacion:confirmar')

    def test_formulario_inicial(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'No encontramos')

    def test_cedula_encontrada_muestra_eventos(self):
        r = self.client.get(self.url, {'cedula': '1020304050'})
        self.assertContains(r, 'Ana Pérez')
        self.assertContains(r, 'Boda')
        self.assertContains(r, 'Feria Tech')

    def test_cedula_no_encontrada(self):
        r = self.client.get(self.url, {'cedula': '55555555'})
        self.assertContains(r, 'No encontramos')

    def test_cedula_invalida(self):
        r = self.client.get(self.url, {'cedula': 'abc'})
        self.assertContains(r, 'Escribe solo números')
