import base64
import datetime
import json
from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, tag
from django.urls import reverse
from django.utils import timezone

from proj.models import Korisnik, dohvatiSveTrenere, Komentar, Trening, Drzi, dohvatiOdgovarajucegTrenera, Paket, \
    Pretplata, Obuhvata, Prati, Termin, Podrzava, Sala, Pokriva

'''
from proj.models import Korisnik, dohvatiSveTrenere


# Create your tests here.

class DohvatiSveTrenereTest(TestCase):
    def setUp(self):
        k = Korisnik.objects.create(mejl='David', sifra='Duric123456', uloga='trener')
        self.expected = []
        self.expected.append({'idkor': k.idkor, 'mejl': k.mejl, 'uloga': k.uloga, 'sifra': k.sifra, 'slika': k.slika})
        k = Korisnik.objects.create(mejl='Mila', sifra='Pantic123456', uloga='trener')
        self.expected.append({'idkor': k.idkor, 'mejl': k.mejl, 'uloga': k.uloga, 'sifra': k.sifra, 'slika': k.slika})
        k = Korisnik.objects.create(mejl='Kristina', sifra='Kragovic123456', uloga='clan')
        #self.expected.append({'idkor': k.idkor, 'mejl': k.mejl, 'uloga': k.uloga, 'sifra': k.sifra, 'slika': k.slika})

    def test_dohvati_sve_trenere(self):
        results = dohvatiSveTrenere()
        self.assertEquals(results, self.expected)

class UkloniTreneraTest(TestCase):

    def setUp(self):
        k = Korisnik.objects.create(mejl='David', sifra='Duric123456', uloga='trener')
        self.expected = []
        self.expected.append({'idkor': k.idkor, 'mejl': k.mejl, 'uloga': k.uloga, 'sifra': k.sifra, 'slika': k.slika})
        k = Korisnik.objects.create(mejl='Mila', sifra='Pantic123456', uloga='trener')
        self.to_delete = k.idkor
        #self.expected.append({'idkor': k.idkor, 'mejl': k.mejl, 'uloga': k.uloga, 'sifra': k.sifra, 'slika': k.slika})
        Korisnik.objects.create(mejl='Kristina', sifra='Kragovic123456', uloga='clan')

'''
# Client je fake browser, sluzi da salje zahtjeve i testira


'''TESTIRANJE UREDI TRENERA David Duric 2021/0102 '''

class UrediTrenera(TestCase):

    def setUp(self):
        self.client = Client()

    def test_uredi_trenera_dodaj_trening_bez_slike(self):
        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()

        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)
        k2 = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        u = User.objects.create(username='trener')
        u.set_password('1234567890')
        u.save()
        id = k2.idkor
        dohvacen_korisnik = Korisnik.objects.filter(idkor=id)
        self.assertTrue(dohvacen_korisnik)

        trening = Trening.objects.create(idtre=1, tip='TestTrening')
        #drzi = Drzi.objects.create(idtre1=trening, idkor=k2)
        trening.save()
        #drzi.save()

        response = self.client.get(reverse('urediTrenera'))

        self.assertEqual(response.status_code, 200)


        response = self.client.post(reverse('urediOdgovarajucegTrenera', kwargs={'id_tr': id}))

        self.assertEqual(response.status_code, 200)

        form_data = {
             f'item{trening.idtre}': 'on',
            'trener_id': str(id),
            'image': '',
        }
        print('FORMDATA', form_data)

        self.client.post(reverse('primeniPromeneNadTrenerom'), form_data)
        drzi = Drzi.objects.filter(idtre1=trening, idkor=k2)
        self.assertTrue(drzi, 'Trening nije ispravno dodat')

        self.client.get(reverse('logout'))

        print('TEST14 OK')


    def test_uredi_trenera_samo_slika(self):
        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()

        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)
        k2 = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        u = User.objects.create(username='trener')
        u.set_password('1234567890')
        u.save()
        id = k2.idkor
        dohvacen_korisnik = Korisnik.objects.filter(idkor=id)

        self.assertTrue(dohvacen_korisnik)



        response = self.client.get(reverse('urediTrenera'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('urediOdgovarajucegTrenera', kwargs={'id_tr': id}))
        self.assertEqual(response.status_code, 200)

        image_path = 'slike_trenera/1-01.jpg'
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        image = SimpleUploadedFile(name='test_image.jpg', content=image_data, content_type='image/jpeg')

        form_data = {
            'trener_id': str(id),
            'image': image,
        }

        self.client.post(reverse('primeniPromeneNadTrenerom'), form_data)

        with open(image_path, 'rb') as original_image_file:
            original_image_data = original_image_file.read()

        updated_trener = Korisnik.objects.get(idkor=id)

        stored_image_data = updated_trener.slika
        self.assertEqual(original_image_data, stored_image_data, "Postavljena slika nije jednaka predatoj")

        self.client.get(reverse('logout'))
        print("TEST15 OK")


    def test_uredi_trenera_sve(self):
        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()

        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)
        k2 = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        u = User.objects.create(username='trener')
        u.set_password('1234567890')
        u.save()
        id = k2.idkor
        trening = Trening.objects.create(idtre=1, tip='TestTrening')
        # drzi = Drzi.objects.create(idtre1=trening, idkor=k2)
        trening.save()

        dohvacen_korisnik = Korisnik.objects.filter(idkor=id)

        self.assertTrue(dohvacen_korisnik)

        response = self.client.get(reverse('urediTrenera'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('urediOdgovarajucegTrenera', kwargs={'id_tr': id}))
        self.assertEqual(response.status_code, 200)

        image_path = 'slike_trenera/1-01.jpg'
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        image = SimpleUploadedFile(name='test_image.jpg', content=image_data, content_type='image/jpeg')

        form_data = {
             f'item{trening.idtre}': 'on',
            'trener_id': str(id),
            'image': image,
        }

        self.client.post(reverse('primeniPromeneNadTrenerom'), form_data)

        with open(image_path, 'rb') as original_image_file:
            original_image_data = original_image_file.read()

        updated_trener = Korisnik.objects.get(idkor=id)

        stored_image_data = updated_trener.slika
        self.assertEqual(original_image_data, stored_image_data, "Postavljena slika nije jednaka predatoj")

        drzi = Drzi.objects.filter(idtre1=trening, idkor=k2)
        self.assertTrue(drzi, 'Trening nije ispravno dodat')

        self.client.get(reverse('logout'))
        print("TEST16 OK")

'''TESTIRANJE KOMENTARA - 12 TESTOVA David Duric 2021/0102'''
class TestGostKomentar(TestCase):
    def setUp(self):
        self.client = Client()
        self.gost_komentar_url = reverse("gostKomentar")
    def test_gost_komentar(self):

        response = self.client.get(self.gost_komentar_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/gost_o_nama.html')
        self.client.get(reverse('logout'))
        print("TEST1 OK")

class TestKorisnikKomentar(TestCase):

    def setUp(self):
        self.client = Client()
        self.korisnik_komentar_url = reverse("korisnikKomentar")

    def test_korisnik_komentar(self):
        '''Funkcija provjerava da li korisnik dobija odgovarajucu stranicu. Ako to nije slucaj, test pada.'''
        Korisnik.objects.create(mejl='korisnik1@gmail.com', sifra='123', uloga='clan')
        u = User.objects.create(username='korisnik1@gmail.com')
        pword = '123'
        u.set_password(pword)
        u.save()
        login = self.client.login(username=u.username, password=pword)
        self.assertTrue(login)

        response = self.client.get(self.korisnik_komentar_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/korisnik_komentari.html')
        self.client.get(reverse('logout'))
        print("TEST2 OK")
    def test_korisnik_komentar_trener(self):
        '''Funkcija provjerava da trener ne moze da pristupi stranici komentari korisnika'''
        Korisnik.objects.create(mejl='korisnik2@gmail.com', sifra='123', uloga='trener')
        u = User.objects.create(username='korisnik2@gmail.com')
        pword = '123'
        u.set_password(pword)
        u.save()
        login = self.client.login(username=u.username, password=pword)
        self.assertTrue(login)

        response = self.client.get(self.korisnik_komentar_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'Better luck next time :)', response.content)
        self.client.get(reverse('logout'))
        print("TEST3 OK")

    def test_korisnik_komentari_trenera(self):
        '''Korisnik moze da klikne na konkretnog trenera i da udje u njegove komentare'''
        Korisnik.objects.create(mejl='korisnik1@gmail.com', sifra='123', uloga='clan')
        k = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        u = User.objects.create(username='korisnik1@gmail.com')
        pword = '123'
        u.set_password(pword)
        u.save()
        login = self.client.login(username=u.username, password=pword)
        self.assertTrue(login)

        response = self.client.get(self.korisnik_komentar_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/korisnik_komentari.html')

        self.trener_komentar_url = reverse("trenerKorisnik", kwargs={'trener_id': k.idkor})

        response = self.client.get(self.trener_komentar_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/komentarisanTrenerKorisnik.html')

        self.client.get(reverse('logout'))
        print("TEST10 OK")

    def test_korisnik_ostavlja_komentar_o_teretani(self):
        '''Korisnik ostavlja komentar o teretani'''
        Korisnik.objects.create(mejl='korisnik1@gmail.com', sifra='123', uloga='clan')
        k = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        u = User.objects.create(username='korisnik1@gmail.com')
        pword = '123'
        u.set_password(pword)
        u.save()
        login = self.client.login(username=u.username, password=pword)
        self.assertTrue(login)

        response = self.client.get(reverse('ostaviKomentar'))

        form_data = {
            'komentar': 'Ovo je test komentar',
            'trener': 'teretana'
        }

        response = self.client.post(reverse('ostaviKomentar'), form_data)

        komentari = Komentar.objects.get(tekst='Ovo je test komentar')

        self.assertTrue(komentari)

        response = self.client.get(self.korisnik_komentar_url)
        # nije odobreno pa ne bi trebalo da se vidi
        self.assertNotIn(b'Ovo je test komentar', response.content)

        self.client.get(reverse('logout'))
        print("TEST11 OK")

    def test_korisnik_ostavlja_komentar_o_treneru(self):
        Korisnik.objects.create(mejl='korisnik1@gmail.com', sifra='123', uloga='clan')
        k = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        u = User.objects.create(username='korisnik1@gmail.com')
        pword = '123'
        u.set_password(pword)
        u.save()
        login = self.client.login(username=u.username, password=pword)
        self.assertTrue(login)

        response = self.client.get(reverse('ostaviKomentar'))

        form_data = {
            'komentar': 'Ovo je test komentar',
            'trener': str(k.idkor)
        }

        response = self.client.post(reverse('ostaviKomentar'), form_data)

        komentari = Komentar.objects.get(tekst='Ovo je test komentar')

        self.assertTrue(komentari)

        response = self.client.get(self.korisnik_komentar_url)
        # nije odobreno pa ne bi trebalo da se vidi
        self.assertNotIn(b'Ovo je test komentar', response.content)

        print("TEST12 OK")
        self.client.get(reverse('logout'))

class TrenerTreneroviKomentari(TestCase):
    def setUp(self):
        self.client = Client()

    def test_trener(self):
        '''Trener moze da pristupi svojim komentarima'''
        k = Korisnik.objects.create(mejl='korisnik2@gmail.com', sifra='123', uloga='trener')
        u = User.objects.create(username='korisnik2@gmail.com')
        self.trener_komentar_url = reverse("trenerTrener", kwargs={'trener_id': k.idkor})
        pword = '123'
        u.set_password(pword)
        u.save()
        login = self.client.login(username=u.username, password=pword)
        self.assertTrue(login)
        response = self.client.get(self.trener_komentar_url)

        self.assertEqual(response.status_code, 200)
        self.client.get(reverse('logout'))
        print("TEST4 OK")

class AdminOdobravanjeKomentara(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_komentar = reverse('odobriKomentarPregled')

    def test_privilegija_admina(self):
        '''Clan ne moze da odobrava komentare'''
        k1 = Korisnik.objects.create(mejl='korisnik@g', sifra='123', uloga='clan')
        u = User.objects.create(username='korisnik@g')
        u.set_password('123')
        u.save()

        login = self.client.login(username=u.username, password='123')
        self.assertTrue(login)

        response = self.client.get(self.admin_komentar)
        #print(response.content)
        self.assertEqual(b'Better luck next time :)', response.content)
        self.client.get(reverse('logout'))
        print("TEST5 OK")
    def test_privilegija_admina_trener(self):
        '''Trener ne moze da odobrava komentare'''
        k1 = Korisnik.objects.create(mejl='korisnik@g', sifra='123', uloga='trener')
        u = User.objects.create(username='korisnik@g')
        u.set_password('123')
        u.save()

        login = self.client.login(username=u.username, password='123')
        self.assertTrue(login)

        response = self.client.get(self.admin_komentar)
        #print(response.content)
        self.assertEqual(b'Better luck next time :)', response.content)
        self.client.get(reverse('logout'))
        print("TEST6 OK")

    def test_admin_pregled_komentara_za_odobravanje_nema(self):
        '''Admin nema nijedan komentar za odobravanje'''
        k1 = Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()

        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)

        response = self.client.get(self.admin_komentar)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nema komentara za odobravanje', response.content)
        self.client.get(reverse('logout'))
        print("TEST7 OK")


    def test_admin_pregled_komentara_za_odobravanje_ima(self):
        '''Admin pregleda komentare i ima komentara'''
        k1 = Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()

        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)

        k = Korisnik.objects.create(mejl='korisnik1@gmail.com', sifra='123', uloga='clan')
        kom = Komentar.objects.create(tekst='TestKomentar', status=0, idautor=k, idkomentarisan=k1,
                                      datum=datetime.datetime.now(datetime.timezone.utc))

        k.save()
        kom.save()

        response = self.client.get(self.admin_komentar)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestKomentar', response.content)
        self.assertNotIn(b'Nema komentara za odobravanje', response.content)
        self.assertTemplateUsed(response, 'proj/admin_komentari.html')

        self.client.get('logout')
        print("TEST8 OK")

    def test_admin_pregled_odobri_komentar(self):
        '''Admin odobrava komentare. Nakon odobravanja, u bazi ostaje odobren komentar, a neodobreni ne postoji.
           Status odobrenog komentara je 1, a vise nema komentara za odobravanje'''
        k1 = Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()

        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)

        k = Korisnik.objects.create(mejl='korisnik1@gmail.com', sifra='123', uloga='clan')
        kom_bice_odobren = Komentar.objects.create(tekst='KomentarBiceOdobren', status=0, idautor=k, idkomentarisan=k1,
                                      datum=datetime.datetime.now(datetime.timezone.utc))
        kom_nece_biti_odobren = Komentar.objects.create(tekst='KomentarNeceBitiOdobren', status=0, idautor=k, idkomentarisan=k1,
                                      datum=datetime.datetime.now(datetime.timezone.utc))
        k.save()
        kom_bice_odobren.save()
        kom_nece_biti_odobren.save()

        self.client.get(self.admin_komentar)

        form_data = {
            f'item{kom_bice_odobren.idkom}': 'on'
        }
        response = self.client.post(reverse('odobriKomentar'), form_data)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.admin_komentar)
        self.assertIn(b'Nema komentara za odobravanje', response.content)

        odobren_komentar = Komentar.objects.get(idkom=kom_bice_odobren.idkom, status=1)
        self.assertEqual(odobren_komentar.tekst, 'KomentarBiceOdobren')

        neodobren_komentar = Komentar.objects.filter(idkom=kom_nece_biti_odobren.idkom)
        self.assertFalse(neodobren_komentar)

        self.client.get(reverse('logout'))
        print("TEST9 OK")


'''TESTIRANJE UKLONI TRENERA 1 TEST David Duric 2021/0102'''

class UklanjanjeTrenera(TestCase):
    def setUp(self):
        self.client = Client()

    def test_uklanjanje_trenera(self):
        #Provjera da se trener uklanja, kao i veze iz tabele Drzi.
        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()

        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)
        k2 = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        u = User.objects.create(username='trener')
        u.set_password('1234567890')
        u.save()
        id = k2.idkor
        dohvacen_korisnik = Korisnik.objects.filter(idkor=id)
        self.assertTrue(dohvacen_korisnik)

        trening = Trening.objects.create(tip='TestTrening')
        drzi = Drzi.objects.create(idtre1=trening, idkor=k2)
        trening.save()
        drzi.save()

        response = self.client.get(reverse('ukloniTrenera'))

        form_data = {
            'trener_id': str(id)
        }

        response = self.client.post(reverse('ukloniTreneraPrimeni'), form_data)

        dohvacen_korisnik = Korisnik.objects.filter(idkor=id)
        self.assertFalse(dohvacen_korisnik)

        dohvaceno_drzi = Drzi.objects.filter(idkor__idkor=id)
        self.assertFalse(dohvaceno_drzi)

        self.client.get(reverse('logout'))
        print("TEST13 OK")

'''Sofija Martinovic, 0486/2021 - Test odjavljivanje admina sa sistema'''

@tag("sofija")
class LogoutUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='user')

    def test_logout_user(self):
        login = self.client.login(username='user', password='user')
        self.assertTrue(login)

        response = self.client.get(reverse('index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        response = self.client.get(reverse('index'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        print("TEST_LOGOUT_USER OK")

'''Sofija Martinovic, 0486/2021 - Test dodavanje treninga GET zahtev'''

@tag("sofija")
class DodajTreningPregledTest(TestCase):

    def setUp(self):
        self.client = Client()
        k1 = Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        self.url = reverse('dodajTreningPregled')

    def test_dodaj_trening_pregled_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'proj/admin_dodajTrening.html')

        self.assertEqual(response.context['provera'], 3)

        print("TEST_DODAJ_TRENING_PREGLED_GET OK")

'''Sofija Martinovic, 0486/2021 - Test dodavanje treninga POST zahtev'''

@tag("sofija")
class DodavanjeTreningaTest(TestCase):

    def setUp(self):
        self.client = Client()
        k = Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()
        login = self.client.login(username='admin', password='admin')
        self.assertTrue(login)
        self.url = reverse('dodavanjeTreninga')

    def test_dodavanje_treninga_post(self):
        post_data = {
            'tip_treninga': 'Yoga'
        }

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'proj/admin_dodajTrening.html')

        self.assertEqual(response.context['provera'], False)

        print("TEST_DODAVANJE_TRENINGA_POST OK")

'''Sofija Martinovic, 0486/2021 - Test pretplata korisnika na odabrani paket'''

@tag("sofija")
class PaketiKorisnikaOdabranPaketTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.korisnik = Korisnik.objects.create(mejl='ms210486d@student.etf.bg.ac.rs', uloga='clan', sifra='123')
        self.user = User.objects.create_user(username='ms210486d@student.etf.bg.ac.rs', password='123')
        self.client.login(username='ms210486d@student.etf.bg.ac.rs', password='123')
        self.url = reverse('paketiKorisnikaOdabranPaket')
        self.paket = Paket.objects.create(naziv='Novi paket', cena=1000.00, brtermina=10, dana=30)

        # Binding the user and the custom Korisnik model
        self.korisnik.user = self.user
        self.korisnik.save()

    def test_postoji_pretplata(self):
        Pretplata.objects.create(
            datumdo=datetime.datetime.now() + datetime.timedelta(days=30),
            preostalotermina=10,
            idpretplaceni=self.korisnik
        )

        response = self.client.post(
            self.url,
            data=json.dumps({'paket_naziv': self.paket.naziv}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['message'], 'Aktivna pretplata jos uvek postoji')
        self.assertFalse(response_data['success'])

    def test_uspesno_pretplata(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'paket_naziv': self.paket.naziv}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['message'], f'Uspesno ste pretplaceni na paket {self.paket.naziv}')
        self.assertTrue(response_data['success'])

'''Sofija Martinovic, 0486/2021 - Test logovanja GET metod'''

@tag("sofija")
class GoToLoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')  # Pretpostavljamo da je URL povezan sa 'go_to_login' funkcijom

    def test_go_to_login(self):
        '''Test da li funkcija vraća login stranicu sa statusom 200'''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/pocetna.html')
        print("TEST go_to_login OK")

'''Sofija Martinovic, 0486/2021 - Test logovanje korisnika'''

@tag("sofija")
class LoginUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login_user')

        self.trener_user = User.objects.create_user(username='trener@example.com', password='trener')
        self.clan_user = User.objects.create_user(username='clan@example.com', password='clan')
        self.admin_user = User.objects.create_user(username='admin@example.com', password='admin')

        self.trener_korisnik = Korisnik.objects.create(mejl='trener@example.com', sifra='trener', uloga='trener')
        self.clan_korisnik = Korisnik.objects.create(mejl='clan@example.com', sifra='clan', uloga='clan')
        self.admin_korisnik = Korisnik.objects.create(mejl='admin@example.com', sifra='admin', uloga='admin')

    def test_uspesno_logovanje_trenera(self):
        response = self.client.post(self.url, {'username': 'trener@example.com', 'password': 'trener'})
        self.assertEqual(response.status_code, 302)

    def test_uspesno_logovanje_clana(self):
        response = self.client.post(self.url, {'username': 'clan@example.com', 'password': 'clan'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('korisnikPocetna'))

    def test_uspesno_logovanje_admina(self):
        response = self.client.post(self.url, {'username': 'admin@example.com', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('adminPocetna'))

    def test_korIme_postoji(self):
        response = self.client.post(self.url, {'username': 'nonexistent@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Korisničko ime ne postoji.")

    def test_lozinka_nije_ispravna(self):
        response = self.client.post(self.url, {'username': 'trener@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lozinka nije ispravna!')

    def test_trener_pocetna_dohvata(self):
        self.client.login(username='trener@example.com', password='trener')
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/pocetna.html')
        print("TEST_TRENER_POCETNA_GET OK")

'''Sofija Martinovic, 0486/2021 - Test registracija GET zahtev'''

@tag("sofija")
class RegistracijaViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('registracija')

    def test_registracija_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/registracija.html')
        print("TEST_REGISTRACIJA_UCITANA_STR OK")

'''Sofija Martinovic, 0486/2021 - Test registracija uspesna'''

@tag("sofija")
class RegistracijaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('registrujSe')
        self.valid_user_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword'
        }

    @patch('proj.views.korisnikPostoji')
    @patch('proj.views.Redis')
    def test_korisnik_postoji(self, mock_redis, mock_korisnikPostoji):
        mock_korisnikPostoji.return_value = True
        response = self.client.post(self.url, self.valid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/registracija.html')
        self.assertTrue(response.context['porukaGreske'])

    @patch('proj.views.korisnikPostoji')
    @patch('proj.views.Redis')
    def test_slanje_fajla_od_redisa(self, mock_redis, mock_korisnikPostoji):
        mock_korisnikPostoji.return_value = False
        mock_redis_instance = Mock()
        mock_redis_instance.setnx.return_value = False
        mock_redis.return_value.__enter__.return_value = mock_redis_instance

        response = self.client.post(self.url, self.valid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/registracija.html')
        self.assertTrue(response.context['porukaGreske'])

    @patch('proj.views.korisnikPostoji')
    @patch('proj.views.Redis')
    @patch('proj.views.code_mail')
    @patch('proj.views.random.randint')
    def test_uspesna_registracija(self, mock_randint, mock_code_mail, mock_redis, mock_korisnikPostoji):
        mock_korisnikPostoji.return_value = False
        mock_redis_instance = Mock()
        mock_redis_instance.setnx.return_value = True
        mock_redis.return_value.__enter__.return_value = mock_redis_instance
        mock_randint.return_value = 12345

        response = self.client.post(self.url, self.valid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/registracija.html')
        self.assertTrue(response.context['show_popup'])
        mock_code_mail.assert_called_once_with(self.valid_user_data['username'], 12345)
        mock_redis_instance.set.assert_called_once_with(
            f"{self.valid_user_data['username']}:12345",
            self.valid_user_data['password'],
            ex=120
        )
        self.assertIn('username', response.cookies)
        self.assertEqual(response.cookies['username'].value, self.valid_user_data['username'])

'''Sofija Martinovic, 0486/2021 - Test za potvrdu koda'''

@tag("sofija")
class PotvrdaKodaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('potvrdaKoda')
        self.valid_user_data = {
            'authCode': 12345
        }
        self.invalid_user_data = {
            'authCode': 54321
        }
        self.korisnickiMejl = 'testuser@example.com'
        self.korisnickaLozinka = 'testpassword'
        self.client.cookies['username'] = self.korisnickiMejl

    @patch('proj.views.registracija_korisnika')
    @patch('proj.views.Redis')
    def test_potvrda_koda_validno(self, mock_redis, mock_registracija_korisnika):
        mock_redis_instance = Mock()
        mock_redis_instance.getdel.return_value = self.korisnickaLozinka.encode()
        mock_redis.return_value.__enter__.return_value = mock_redis_instance

        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        mock_registracija_korisnika.assert_called_once_with(self.korisnickiMejl, self.korisnickaLozinka)
        self.assertEqual(response.cookies.get('username').value, '')

    @patch('proj.views.registracija_korisnika')
    @patch('proj.views.Redis')
    def test_potvrda_koda_nevalidno(self, mock_redis, mock_registracija_korisnika):
        mock_redis_instance = Mock()
        mock_redis_instance.getdel.return_value = None
        mock_redis.return_value.__enter__.return_value = mock_redis_instance

        response = self.client.post(
            self.url,
            data=json.dumps(self.invalid_user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False})
        mock_registracija_korisnika.assert_not_called()

    @patch('proj.views.registracija_korisnika')
    @patch('proj.views.Redis')
    def test_potvrda_koda_uzimanje_zahteva(self, mock_redis, mock_registracija_korisnika):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False})
        mock_redis.assert_not_called()
        mock_registracija_korisnika.assert_not_called()

'''TESTIRANJE DODAVANJE PAKETA Kristina Kragovic 0270/2021'''
class PaketTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dodavanje_paketa_uspesno(self):

        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()
        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)


        trening1 = Trening.objects.create(idtre=1, tip='TestTrening1')
        trening2 = Trening.objects.create(idtre=2, tip='TestTrening2')


        form_data = {
            'nazivPaketa': 'Test Paket',
            'brojTermina': '10',
            'brojDana': '30',
            'cenaPaketa': '1000',
            'item1': 'on',
            'item2': 'on',
        }


        response = self.client.post(reverse('dodavanjePaketa'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/admin_dodajPaket.html')
        self.assertContains(response, 'paket')


        paket = Paket.objects.get(naziv='Test Paket')
        self.assertIsNotNone(paket)
        self.assertEqual(paket.cena, 1000)
        self.assertEqual(paket.brtermina, 10)
        self.assertEqual(paket.dana, 30)


        obuhvata_trening1 = Obuhvata.objects.get(idpak=paket, idtre=trening1)
        obuhvata_trening2 = Obuhvata.objects.get(idpak=paket, idtre=trening2)
        self.assertIsNotNone(obuhvata_trening1)
        self.assertIsNotNone(obuhvata_trening2)
        print('TEST_DODAJ_PAKET OK')
    def test_dodavanje_paketa_duplikat(self):

        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        u = User.objects.create(username='admin')
        u.set_password('admin')
        u.save()
        login = self.client.login(username=u.username, password='admin')
        self.assertTrue(login)


        Paket.objects.create(naziv='Test Paket', cena=1000, brtermina=10, dana=30)


        form_data = {
            'nazivPaketa': 'Test Paket',
            'brojTermina': '10',
            'brojDana': '30',
            'cenaPaketa': '1000',
        }


        response = self.client.post(reverse('dodavanjePaketa'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/admin_dodajPaket.html')
        self.assertContains(response, '-1')
        print('TEST_DODAJ_PAKET_IME_VEC_POSTOJI OK')

'''TESTIRANJE UREDJIVANJE PAKETA Kristina Kragovic 0270/2021'''
class PaketUpdateTests(TestCase):

    def setUp(self):
        self.client = Client()

        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        self.user = User.objects.create(username='admin')
        self.user.set_password('admin')
        self.user.save()
        self.client.login(username=self.user.username, password='admin')

        self.trening1 = Trening.objects.create(idtre=1, tip='TestTrening1')
        self.trening2 = Trening.objects.create(idtre=2, tip='TestTrening2')
        self.trening3 = Trening.objects.create(idtre=3, tip='TestTrening3')
        self.paket = Paket.objects.create(naziv='Initial Paket', cena=1000, brtermina=10, dana=30)


    def test_uredi_paket_uspesno(self):
        form_data = {
            'paket_id': self.paket.idpak,
            'br_termina': '15',
            'br_dana': '40',
            'cena': '1500',
            'naziv_paket': 'Updated Paket',
            'TestTrening1': 'on',
            'TestTrening3': 'on',
        }



        response = self.client.post(reverse('novaForma'), form_data)
        self.assertRedirects(response, '/adminPocetna')

        updated_paket = Paket.objects.get(idpak=self.paket.idpak)
        self.assertEqual(updated_paket.naziv, 'Updated Paket')
        self.assertEqual(updated_paket.cena, 1500)
        self.assertEqual(updated_paket.brtermina, 15)
        self.assertEqual(updated_paket.dana, 40)


        updated_treninzi = Obuhvata.objects.filter(idpak=updated_paket).values_list('idtre__tip', flat=True)
        self.assertIn('TestTrening1', updated_treninzi)
        self.assertIn('TestTrening3', updated_treninzi)
        self.assertNotIn('TestTrening2', updated_treninzi)
        print('TEST_UREDJIVANJE_PAKETA OK')
    def test_uredi_paket_duplikat_naziv(self):
        Paket.objects.create(naziv='Existing Paket', cena=1200, brtermina=12, dana=32)

        form_data = {
            'paket_id': self.paket.idpak,
            'br_termina': '15',
            'br_dana': '40',
            'cena': '1500',
            'naziv_paket': 'Existing Paket',
        }

        Obuhvata.objects.filter(idpak=self.paket).delete()

        response = self.client.post(reverse('novaForma'), form_data)
        self.assertRedirects(response, '/adminPocetna')

        paket = Paket.objects.get(idpak=self.paket.idpak)
        self.assertEqual(paket.naziv, 'Initial Paket')
        print('TEST_UREDJIVANJE_PAKETA_NAZIV_POSTOJI OK')

'''TESTIRANJE BRISANJA PAKETA Kristina Kragovic 0270/2021'''
class PaketDeletionTest(TestCase):

    def setUp(self):
        self.client = Client()
        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        self.user = User.objects.create(username='admin')
        self.user.set_password('admin')
        self.user.save()
        self.client.login(username=self.user.username, password='admin')

        self.paket1 = Paket.objects.create(naziv='Paket 1', cena=1000, brtermina=10, dana=30)
        self.paket2 = Paket.objects.create(naziv='Paket 2', cena=1500, brtermina=15, dana=45)

    def test_ukloni_paket_uspesno(self):
        response = self.client.get(reverse('ukloniPaket'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/admin_ukloniPaket.html')
        self.assertContains(response, 'Paket 1')
        self.assertContains(response, 'Paket 2')

        form_data = {
            'paket': 'Paket 1'
        }
        response = self.client.post(reverse('ukloniPaketPrimeni'), form_data)
        self.assertRedirects(response, '/adminPocetna')

        with self.assertRaises(Paket.DoesNotExist):
            Paket.objects.get(naziv='Paket 1')

        paket2 = Paket.objects.get(naziv='Paket 2')
        self.assertIsNotNone(paket2)
        print('TEST_UKLONI_PAKET OK')

'''TESTIRANJE DODAVANJA TRENERA Kristina Kragovic 0270/2021'''
class DodavanjeTreneraTests(TestCase):

    def setUp(self):
        self.client = Client()

        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        self.user = User.objects.create(username='admin')
        self.user.set_password('admin')
        self.user.save()
        self.client.login(username=self.user.username, password='admin')


        self.trening1 = Trening.objects.create(idtre=1, tip='TestTrening1')
        self.trening2 = Trening.objects.create(idtre=2, tip='TestTrening2')

    def test_dodavanje_trenera_uspesno(self):
        image_path = "../slike_trenera/1-01.jpg"
        with open(image_path, "rb") as img:
            image = SimpleUploadedFile("image.jpg", img.read(), content_type="image/jpeg")

        form_data = {
            'username': 'new_trainer',
            'password': 'password123',
            'item1': 'on',
            'item2': 'on',
            'image': image
        }

        response = self.client.post(reverse('dodavanjeTrenera'), data=form_data, follow=True, files={'image': image})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/admin_dodajTrenera.html')

        trener = Korisnik.objects.get(mejl='new_trainer')
        self.assertIsNotNone(trener)
        self.assertEqual(trener.uloga, 'trener')

        drzi_treninzi = Drzi.objects.filter(idkor=trener).values_list('idtre1__tip', flat=True)
        self.assertIn('TestTrening1', drzi_treninzi)
        self.assertIn('TestTrening2', drzi_treninzi)

        user = User.objects.get(username='new_trainer')
        self.assertIsNotNone(user)
        print('TEST_DODAVANJE_TRENERA OK')

    def test_dodavanje_trenera_duplikat_korisnicko_ime(self):
        User.objects.create_user(username='existing_trainer', password='password123')

        image_path = "../slike_trenera/1-01.jpg"
        with open(image_path, "rb") as img:
            image = SimpleUploadedFile("image.jpg", img.read(), content_type="image/jpeg")

        form_data = {
            'username': 'existing_trainer',
            'password': 'password123',
            'item1': 'on',
            'image': image
        }


        response = self.client.post(reverse('dodavanjeTrenera'), data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/admin_dodajTrenera.html')

        with self.assertRaises(Korisnik.DoesNotExist):
            Korisnik.objects.get(mejl='existing_trainer')

        users = User.objects.filter(username='existing_trainer')
        self.assertEqual(users.count(), 1)
        print('TEST_DOVANJE_TRENERA_IME_ZAUZETO OK')

'''TESTIRANJE PREGLEDA PRISUTNIH Kristina Kragovic 0270/2021'''
class PregledPrisutnihTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin_user = User.objects.create_user(username='admin', password='admin')
        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        self.client.login(username='admin', password='admin')

        self.trener_korisnik = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        self.trener_user = User.objects.create_user(username='trener', password='1234567890')
        self.client.login(username='trener', password='1234567890')

        self.sala = Sala.objects.create(naziv='Sala 1')
        self.trening1 = Trening.objects.create(tip='Trening 1')
        self.trening2 = Trening.objects.create(tip='Trening 2')

        self.podrzava = Podrzava.objects.create(idsala=self.sala, idtre2=self.trening2)
        self.drzi = Drzi.objects.create(idkor=self.trener_korisnik, idtre1=self.trening1)

        self.korisnik1 = Korisnik.objects.create(mejl='korisnik1@example.com', sifra='sifra1', uloga='clan')
        self.korisnik2 = Korisnik.objects.create(mejl='korisnik2@example.com', sifra='sifra2', uloga='clan')
        self.termin = Termin.objects.create(
            dan='Mon',
            pocetak='10:00:00',
            kraj='11:00:00',
            idpodrzava=self.podrzava,
            iddrzi=self.drzi,
            preostalo=10
        )
        Prati.objects.create(idkor=self.korisnik1, idter=self.termin)
        Prati.objects.create(idkor=self.korisnik2, idter=self.termin)


    def test_pregled_prisutnih(self):

        form_data = {
            'idter': self.termin.idter,
        }

        response = self.client.post(reverse('pregledPrisutnih'), form_data)

        print(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/trener_evidencija.html')
        self.assertContains(response, 'korisnik1@example.com')
        self.assertContains(response, 'korisnik2@example.com')

        self.assertIn('korisnik', response.context)
        self.assertIn('id_termina', response.context)
        self.assertIn('parovi', response.context)

        korisnik = response.context['korisnik']
        self.assertEqual(korisnik.mejl, 'trener')

        id_termina = response.context['id_termina']
        self.assertEqual(id_termina, self.termin.idter)

        parovi = response.context['parovi']
        self.assertEqual(len(parovi), 2)
        self.assertEqual(parovi[0][0].idkor.mejl, 'korisnik1@example.com')
        self.assertEqual(parovi[1][0].idkor.mejl, 'korisnik2@example.com')
        print('TEST_EVIDENCIJA_PRISUSTVA OK')

'''TESTIRANJE IZBACIVANJA TRENERA Kristina Kragovic 0270/2021'''
class IzbacivanjeSaTerminaTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin_user = User.objects.create_user(username='admin', password='admin')
        Korisnik.objects.create(mejl='admin', sifra='admin', uloga='admin')
        self.client.login(username='admin', password='admin')

        self.trener_korisnik = Korisnik.objects.create(mejl='trener', sifra='1234567890', uloga='trener')
        self.trener_user = User.objects.create_user(username='trener', password='1234567890')
        self.client.login(username='trener', password='1234567890')

        self.sala = Sala.objects.create(naziv='Sala 1')
        self.trening1 = Trening.objects.create(tip='Trening 1')
        self.trening2 = Trening.objects.create(tip='Trening 2')

        self.podrzava = Podrzava.objects.create(idsala=self.sala, idtre2=self.trening2)
        self.drzi = Drzi.objects.create(idkor=self.trener_korisnik, idtre1=self.trening1)

        self.korisnik1 = Korisnik.objects.create(mejl='korisnik1@example.com', sifra='sifra1', uloga='clan')
        self.korisnik2 = Korisnik.objects.create(mejl='korisnik2@example.com', sifra='sifra2', uloga='clan')
        self.termin = Termin.objects.create(
            dan='Mon',
            pocetak='10:00:00',
            kraj='11:00:00',
            idpodrzava=self.podrzava,
            iddrzi=self.drzi,
            preostalo=10
        )
        Prati.objects.create(idkor=self.korisnik1, idter=self.termin)
        Prati.objects.create(idkor=self.korisnik2, idter=self.termin)

    def test_izbacivanje_sa_termina(self):
        form_data = {
            'id_termina': self.termin.idter,
            'id_korisnika': self.korisnik1.idkor,
            'clicked_button': 'Izbaci',
        }

        response = self.client.post(reverse('izbacivanjeSaTermina'), form_data)

        print(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proj/trener_evidencija.html')
        self.assertNotContains(response, 'korisnik1@example.com')
        self.assertContains(response, 'korisnik2@example.com')

        self.assertIn('korisnik', response.context)
        self.assertIn('id_termina', response.context)
        self.assertIn('parovi', response.context)

        korisnik = response.context['korisnik']
        self.assertEqual(korisnik.mejl, 'trener')

        id_termina = int(response.context['id_termina'])
        self.assertEqual(id_termina, self.termin.idter)

        parovi = response.context['parovi']
        self.assertEqual(len(parovi), 1)
        self.assertEqual(parovi[0][0].idkor.mejl, 'korisnik2@example.com')

        prati = Prati.objects.filter(idkor=self.korisnik1, idter=self.termin)
        self.assertFalse(prati.exists())
        print('TEST_IZBACIVANJE_TRENERA OK')


'''TESTIRANJE DODAVANJE TERMINA Aleksandar Ilic 2021/0495'''
class DodavanjeTerminaTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        dummy_image = base64.b64encode(b'R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=').decode('utf-8')
        # slika se napravi kao dummy objekat jer se trazi u trenerPocetna, ali nije neophodna za
        # pokazivanje funkcionalnosti ovog unit testa
        self.trener_user = User.objects.create_user(username='trener', password='trener')
        self.korisnik_trener = Korisnik.objects.create(
            mejl='trener',
            sifra='trener',
            uloga='trener',
            idkor=self.trener_user.id,
            slika=base64.b64decode(dummy_image)
        )
        self.client.login(username='trener', password='trener')
        self.sala = Sala.objects.create(naziv='Test Sala')
        self.trening = Trening.objects.create(tip='TestTrening')
        self.podrzava = Podrzava.objects.create(idsala=self.sala, idtre2=self.trening)
        self.drzi = Drzi.objects.create(idkor=self.korisnik_trener, idtre1=self.trening)

    def test_dodavanje_termina_success(self):
        form_data = {
            'sale': str(self.sala.idsala),
            'dan': 'Ponedeljak',
            'slobodnih': '10',
            'timeStart': '09:00',
            'timeEnd': '10:00',
            'radio': 'TestTrening',
        }

        response = self.client.post(reverse('dodavanjeTermina'), form_data)

        self.assertRedirects(response, '/trenerPocetna')

        termin = Termin.objects.filter(
            iddrzi=self.drzi,
            idpodrzava=self.podrzava,
            dan='PON',
            pocetak="09:00",
            kraj="10:00",
            preostalo=10,
        ).exists()

        self.assertTrue(termin)

    def test_dodavanje_termina_invalid_time(self):
        form_data = {
            'sale': str(self.sala.idsala),
            'dan': 'Ponedeljak',
            'slobodnih': '10',
            'timeStart': '23:00',
            'timeEnd': '10:00',
            'radio': 'TestTrening',
        }

        response = self.client.post(reverse('dodavanjeTermina'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Neodgovarajuca vremena pocetka i kraja')

    def test_dodavanje_termina_sala_zauzeta(self):
        Termin.objects.create(
            iddrzi=self.drzi,
            idpodrzava=self.podrzava,
            dan='PON',
            pocetak="09:00",
            kraj="10:00",
            preostalo=10,
        )

        form_data = {
            'sale': str(self.sala.idsala),
            'dan': 'Ponedeljak',
            'slobodnih': '10',
            'timeStart': '09:30',
            'timeEnd': '10:30',
            'radio': 'TestTrening',
        }
        response = self.client.post(reverse('dodavanjeTermina'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sala je zauzeta u zadatom terminu ili ste Vi zauzeti.')

    def test_dodavanje_termina_negative_seats(self):
        form_data = {
            'sale': str(self.sala.idsala),
            'dan': 'Ponedeljak',
            'slobodnih': '-15',
            'timeStart': '09:00',
            'timeEnd': '10:00',
            'radio': 'TestTrening',
        }
        response = self.client.post(reverse('dodavanjeTermina'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Broj mesta mora da bude pozitivan broj!')

    def test_dodavanje_termina_sala_nepodrzava(self):
        novi_trening = Trening.objects.create(tip='NoviTrening')

        form_data = {
            'sale': str(self.sala.idsala),
            'dan': 'Ponedeljak',
            'slobodnih': '10',
            'timeStart': '09:00',
            'timeEnd': '10:00',
            'radio': 'NoviTrening',
        }

        response = self.client.post(reverse('dodavanjeTermina'), form_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ova sala ne podrzava zadati trening')

    def test_dodavanje_termina_trener_zauzet(self):
        Termin.objects.create(
            iddrzi=self.drzi,
            idpodrzava=self.podrzava,
            dan='PON',
            pocetak="09:00",
            kraj="10:00",
            preostalo=10,
        )

        form_data = {
            'sale': str(self.sala.idsala),
            'dan': 'Ponedeljak',
            'slobodnih': '10',
            'timeStart': '09:30',
            'timeEnd': '10:30',
            'radio': 'TestTrening',
        }

        response = self.client.post(reverse('dodavanjeTermina'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sala je zauzeta u zadatom terminu ili ste Vi zauzeti.')


from django.test import TestCase

'''TESTIRANJE PRIJAVA CLANA NA ODREDJENI TERMIN Aleksandar Ilic 2021/0495'''
class PrijavaNaTerminTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.clan_user = User.objects.create_user(username='clan', password='clan')
        self.korisnik_clan = Korisnik.objects.create(mejl='clan', sifra='clan', uloga='clan', idkor=self.clan_user.id)
        self.client.login(username='clan', password='clan')

        self.trener_user = User.objects.create_user(username='trener', password='trener')
        self.korisnik_trener = Korisnik.objects.create(mejl='trener', sifra='trener', uloga='trener',
                                                       idkor=self.trener_user.id)
        self.sala = Sala.objects.create(naziv='Test Sala')
        self.trening = Trening.objects.create(tip='TestTrening')
        self.podrzava = Podrzava.objects.create(idsala=self.sala, idtre2=self.trening)
        self.drzi = Drzi.objects.create(idkor=self.korisnik_trener, idtre1=self.trening)

        self.termin = Termin.objects.create(
            dan='PON',
            pocetak='09:00',
            kraj='10:00',
            idpodrzava=self.podrzava,
            iddrzi=self.drzi,
            preostalo=10
        )

        self.pretplata = Pretplata.objects.create(
            datumdo=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30),
            preostalotermina=5,
            idpretplaceni=self.korisnik_clan
        )

        self.pokriva = Pokriva.objects.create(
            idpre=self.pretplata,
            idtre=self.trening
        )

        self.drugi_trening = Trening.objects.create(tip='DrugiTrening')
        self.drugi_podrzava = Podrzava.objects.create(idsala=self.sala, idtre2=self.drugi_trening)
        self.drugi_drzi = Drzi.objects.create(idkor=self.korisnik_trener, idtre1=self.drugi_trening)
        self.drugi_termin = Termin.objects.create(
            dan='UTO',
            pocetak='11:00',
            kraj='12:00',
            idpodrzava=self.drugi_podrzava,
            iddrzi=self.drugi_drzi,
            preostalo=10
        )

    def test_prijava_na_termin_uspesna(self):
        form_data = {'idter': self.termin.idter}
        response = self.client.post(reverse('dodajMeUTermin'), json.dumps(form_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Uspesno ste prijavljeni na termin!')

    def test_nema_slobodnih_mesta(self):
        self.termin.preostalo = 0
        self.termin.save()

        form_data = {'idter': self.termin.idter}
        response = self.client.post(reverse('dodajMeUTermin'), json.dumps(form_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Nema slobodnih mesta za prijavu!')

    def test_pretplata_ne_pokriva_trening(self):
        form_data = {'idter': self.drugi_termin.idter}
        response = self.client.post(reverse('dodajMeUTermin'), json.dumps(form_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Vasa pretplata ne pokriva ovaj tip treninga')

    def test_prijava_na_isti_termin(self):
        Prati.objects.create(idkor=self.korisnik_clan, idter=self.termin)

        form_data = {'idter': self.termin.idter}
        response = self.client.post(reverse('dodajMeUTermin'), json.dumps(form_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Pratite zadati termin. Nije dozvoljeno pratiti isti termin dvaput')

    def test_nema_aktivne_pretplate(self):
      #  self.pretplata.datumdo = str(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)),
        self.pretplata.preostalotermina = 0
        self.pretplata.save()

        form_data = {'idter': self.termin.idter}
        response = self.client.post(reverse('dodajMeUTermin'), json.dumps(form_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Nemate aktivnu pretplatu')


from django.test import TestCase, Client

'''TESTIRANJE ODJAVLJIVANJE CLANA SA ODREDJENOG TERMINA Aleksandar Ilic 2021/0495'''
class OdjavaSaTerminaTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.clan_user = User.objects.create_user(username='clan', password='clan')
        self.korisnik_clan = Korisnik.objects.create(mejl='clan', sifra='clan', uloga='clan', idkor=self.clan_user.id)
        self.client.login(username='clan', password='clan')

        self.trener_user = User.objects.create_user(username='trener', password='trener')
        self.korisnik_trener = Korisnik.objects.create(mejl='trener', sifra='trener', uloga='trener',
                                                       idkor=self.trener_user.id)
        self.sala = Sala.objects.create(naziv='Test Sala')
        self.trening = Trening.objects.create(tip='TestTrening')
        self.podrzava = Podrzava.objects.create(idsala=self.sala, idtre2=self.trening)
        self.drzi = Drzi.objects.create(idkor=self.korisnik_trener, idtre1=self.trening)

        self.termin = Termin.objects.create(
            dan='PON',
            pocetak='09:00',
            kraj='10:00',
            idpodrzava=self.podrzava,
            iddrzi=self.drzi,
            preostalo=10
        )

        self.pretplata = Pretplata.objects.create(
            datumdo=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30),
            preostalotermina=5,
            idpretplaceni=self.korisnik_clan
        )

        self.pokriva = Pokriva.objects.create(
            idpre=self.pretplata,
            idtre=self.trening
        )

        Prati.objects.create(idkor=self.korisnik_clan, idter=self.termin)

    def test_odjava_sa_termina_uspesna(self):
        form_data = {'idter': self.termin.idter}
        # reverse od name pravi url i gadja odgovrajucu stranicu POST zahtevom
        response = self.client.post(reverse('izbaciMeIzTermina'), json.dumps(form_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Termin odjavljen')

        self.assertFalse(Prati.objects.filter(idkor=self.korisnik_clan, idter=self.termin).exists())

    def test_odjava_sa_termina_odustao(self):

        self.assertTrue(Prati.objects.filter(idkor=self.korisnik_clan, idter=self.termin).exists())


'''TESTIRANJE BRISANJE TERMINA Aleksandar Ilic 2021/0495'''
class BrisanjeTerminaTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.trener_user = User.objects.create_user(username='trener', password='trener')
        self.korisnik_trener = Korisnik.objects.create(mejl='trener', sifra='trener', uloga='trener',
                                                       idkor=self.trener_user.id)
        self.client.login(username='trener', password='trener')
        self.sala = Sala.objects.create(naziv='Test Sala')
        self.trening = Trening.objects.create(tip='TestTrening')
        self.podrzava = Podrzava.objects.create(idsala=self.sala, idtre2=self.trening)
        self.drzi = Drzi.objects.create(idkor=self.korisnik_trener, idtre1=self.trening)
        #prvo kreiramo termin
        self.termin = Termin.objects.create(
            dan='PON',
            pocetak='09:00',
            kraj='10:00',
            idpodrzava=self.podrzava,
            iddrzi=self.drzi,
            preostalo=10
        )

    def test_brisanje_termina_uspesno(self):
        form_data = {'idter': self.termin.idter}
        response = self.client.post(reverse('ukloniMojTermin'), json.dumps(form_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Termin odjavljen')

        self.assertFalse(Termin.objects.filter(idter=self.termin.idter).exists())

    def test_brisanje_termina_odustao(self):
        #formu ne moramo da saljemo, odustaje se od POST zahteva
        self.assertTrue(Termin.objects.filter(idter=self.termin.idter).exists())