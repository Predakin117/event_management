from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Evento


class EventosViewsTests(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(
            nombre='Feria de Tecnología',
            descripcion='Charlas y talleres.',
            fecha=timezone.now(),
            lugar='Auditorio Principal',
        )

    def test_lista_muestra_eventos(self):
        r = self.client.get(reverse('eventos:lista'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Feria de Tecnología')

    def test_lista_vacia(self):
        Evento.objects.all().delete()
        r = self.client.get(reverse('eventos:lista'))
        self.assertContains(r, 'Todavía no hay eventos')

    def test_detalle_existente(self):
        r = self.client.get(reverse('eventos:detalle', args=[self.evento.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Auditorio Principal')

    def test_detalle_inexistente_da_404(self):
        r = self.client.get(reverse('eventos:detalle', args=[9999]))
        self.assertEqual(r.status_code, 404)
