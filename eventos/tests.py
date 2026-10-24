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


class CrearEventoTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.usuario = get_user_model().objects.create_user('ana', password='clave-segura-123')
        self.url = reverse('eventos:crear')
        self.datos = {
            'nombre': 'Hackathon',
            'descripcion': 'Maratón de código',
            'fecha': '2026-12-01T09:30',
            'lugar': 'Bloque 5',
        }

    def test_sin_sesion_redirige_al_login(self):
        r = self.client.get(self.url)
        self.assertRedirects(r, f"{reverse('login')}?next={self.url}")

    def test_con_sesion_crea_evento(self):
        self.client.login(username='ana', password='clave-segura-123')
        r = self.client.post(self.url, self.datos)
        evento = Evento.objects.get(nombre='Hackathon')
        self.assertRedirects(r, reverse('eventos:detalle', args=[evento.pk]))

    def test_login_desde_el_sitio(self):
        r = self.client.post(reverse('login'), {'username': 'ana', 'password': 'clave-segura-123'})
        self.assertRedirects(r, reverse('eventos:lista'))

    def test_detalle_oculta_invitados_a_anonimos(self):
        evento = Evento.objects.create(nombre='X', fecha=timezone.now(), lugar='Y')
        self.assertNotContains(self.client.get(reverse('eventos:detalle', args=[evento.pk])), 'Agregar invitado')
        self.client.login(username='ana', password='clave-segura-123')
        self.assertContains(self.client.get(reverse('eventos:detalle', args=[evento.pk])), 'Agregar invitado')
