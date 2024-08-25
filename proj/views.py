import base64
from datetime import datetime
from datetime import time
import json
import random

from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

import proj.models
from proj.mail import code_mail, send_new_email

from proj.models import Termin, Podrzava, Drzi, Korisnik, Prati, Trening, sviPaketi, dodajPaket, obrisiPaket, \
    dohvatiNazivePaketa, dohvatiStaNeObuhvata, urediPaket, dodajPretplatuAkoNePostoji, sviTreninzi, dodajTrening, \
    obrisiTrening, dohvatiSveTrenere, dohvatiOdgovarajucegTrenera, dohvatiKomentareOTreneru, dohvatiPretplate, \
    ImaAktivnuPretplatu, sviTermini, licniRaspored, prijaviTermin, dodajTermin, odjaviTermin, ukloniTermin, \
    registracija_korisnika, korisnikPostoji, dodaj_trenera, ukloni_trenera, dohvatanje_id_treninga, uredi_trenera, \
    dohvatiKomentareOTeretani, kreiraj_komentar, sviTreninziKojeTrenerNeDrzi, dohvatiKomentare, \
    dohvatiNeodobreneKomentare, odobriKomentar, obrisiKomentar, dohvatiOdgovarajuciPaket, dohvati_sale, \
    dohvati_treninge_za_paket, sviPrati, pratiOdredjenTermin, pretplateOdredjenogKorisnika, pratiObrisiKorisnika, \
    dohvatiKorisnikaPoId, dohvatiTerminPoId, dohvatiPaketPoId, pokrivaPretplata, drzi_treninge

from redis import Redis

from proj.role_check import role_required


# Create your views here.

def index(request):
    return render(request, "proj/pocetna.html")


def obrada(request):
    return render(request, "proj/obrada.html", {
        "tekst": request.POST["text"],
        "sel": request.POST["sel"]
    })


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('clan')
def korisnikKomentar(request):
    '''

    Data funkcija dohvata stranicu korisnik_komentari.html uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu korinik_komentari

    '''

    sviKorisnici = dohvatiSveTrenere()

    sviKomentari = dohvatiKomentareOTeretani()
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)

    context = {

        'treneri': sviKorisnici,
        'korisnik': korisnik,
        'komentari': sviKomentari

    }

    # print(sviKorisnici)

    return render(request, "proj/korisnik_komentari.html", context)


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('clan')
def trenerKomentar(request):
    '''
    Data funkcija dohvata stranicu trener_komentari.html uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu trener_komentari
    '''

    sviKorisnici = dohvatiSveTrenere()
    sviKomentari = dohvatiKomentareOTeretani()

    context = {
        'treneri': sviKorisnici,
        'komentari': sviKomentari

    }
    # print(sviKorisnici)
    return render(request, "proj/trener_komentari.html", context)


# Aleksandar Ilic, 0495/2021
def trenerGost(request, trener_id):
    '''
    Data funkcija dohvata id odgovarajuceg trenera(za koga su vezani komentari),
    kao i njegove komentare i sliku
    :param request: Zahtev prosledjen serveru
    :param trener_id: Zahtev prosledjen serveru
    :return: povratna vrenost funkcije je html stranica komentarisanTrener,
    na kojoj se nalazi trener sa slikom i izlistanim komentarima
    '''
    trener = dohvatiOdgovarajucegTrenera(trener_id)
    komentari = dohvatiKomentareOTreneru(trener_id)

    slika = base64.b64encode(trener.slika).decode()

    context = {
        'trener': trener,
        'komentari': komentari,
        'slika': slika
    }
    return render(request, "proj/komentarisanTrener.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('clan')
def trenerKorisnik(request, trener_id):
    '''
    Data funkcija dohvata id odgovarajuceg trenera(za koga su vezani komentari),
    kao i njegove komentare i sliku
    :param request: Zahtev prosledjen serveru
    :param trener_id: Zahtev prosledjen serveru
    :return: povratna vrenost funkcije je html stranica komentarisanTrener,
    na kojoj se nalazi trener sa slikom i izlistanim komentarima
    '''
    trener = dohvatiOdgovarajucegTrenera(trener_id)
    komentari = dohvatiKomentareOTreneru(trener_id)
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)
    if trener.slika:
        slika = base64.b64encode(trener.slika).decode()
    else:
        slika = None
#    print(komentari)
    context = {
        'trener': trener,
        'komentari': komentari,
        'slika': slika,
        'korisnik': korisnik
    }
    return render(request, "proj/komentarisanTrenerKorisnik.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('trener')
def trenerTrener(request, trener_id):
    '''
    Data funkcija dohvata id odgovarajuceg trenera(za koga su vezani komentari),
    kao i njegove komentare i sliku
    :param request: Zahtev prosledjen serveru
    :param trener_id: Zahtev prosledjen serveru
    :return: povratna vrenost funkcije je html stranica komentarisanTrener,
    na kojoj se nalazi trener sa slikom i izlistanim komentarima
    '''
    trener = dohvatiOdgovarajucegTrenera(trener_id)
    komentari = dohvatiKomentareOTreneru(trener_id)
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)
    id = korisnik.idkor
    if trener.slika:
        slika = base64.b64encode(trener.slika).decode()
    else:
        slika = None
#    print(komentari)
    context = {
        'korisnik': korisnik,
        'trener': trener,
        'komentari': komentari,
        'slika': slika,
        'id': id

    }
    return render(request, "proj/komentarisanTrenerTrener.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('clan')
def dostupniPaketiKorisnik(request):
    '''
    Data funkcija dohvata sve pakete koji su dostupni korisniku
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu korisnik_paketi
    '''
    paketi = sviPaketi()

    contextData = dohvati_treninge_za_paket(paketi)
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)
#    print(contextData)
    context = {
        'paketi': paketi,
        'korisnik': korisnik
    }
    return render(request, "proj/korisnik_paketi.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
def dostupniPaketiGost(request):
    '''
    Data funkcija dohvata sve pakete koji su dostupni gostu
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu gost_paketi
    '''
    paketi = sviPaketi()
#    print(paketi)
    context = {
        'paketi': paketi
    }
    return render(request, "proj/gost_paketi.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def ukloniPaket(request):
    '''
    Data funkcija dohvata stranicu ukloni_Paket.html uz pomoc GET metode, na kojoj se nalaze izlistani paketi
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_ukloniPaket
    '''
    paketi = sviPaketi();
    context = {
        'paketi': paketi
    }
    return render(request, "proj/admin_ukloniPaket.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def ukloniTrenera(request):
    '''
    Data funkcija dohvata stranicu ukloni_Trenera.html uz pomoc GET metode, na kojoj se nalaze izlistani treneri
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_ukloniTrenera
    '''
    treneri = dohvatiSveTrenere()
    context = {
        'treneri': treneri
    }
    return render(request, "proj/admin_ukloniTrenera.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('clan')
def korisnikPocetna(request):
    '''
    Data funkcija prikazuje pocetnu stranicu korisnika, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu korisnika
    '''

    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)

    termini = sviTermini()
    sale = dohvati_sale()
    if ImaAktivnuPretplatu(korisnik.mejl):
        pretplata = pretplateOdredjenogKorisnika(korisnik.idkor)
#        print("PRETPLATA POKRIVA")

        pokriva_list = pokrivaPretplata(pretplata.idpre)
#        print(pokriva_list)
        # Convert Pokriva records to a list of training IDs for easier use in the template
        pokriva_trening_ids = [p.idtre.idtre for p in pokriva_list]
    else:
        pokriva_trening_ids = []

    day_list = ['PON', 'UTO', 'SRE', 'CET', 'PET', 'SUB', 'NED']
    context = {
        "korisnik": korisnik,
        'sale': sale,
        "termini": termini,
        "dani": day_list,
        "pokriva_trening_ids": pokriva_trening_ids
    }
    return render(request, "proj/korisnik.html", context)
    # id_kor = korisnik.idkor


@login_required(login_url='login')
def get_updated_termini(request):
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)
    termini = sviTermini()

    termini_data = [{
        'Dan': termin['Dan'],
        'Sala': {'naziv': termin['Sala'].naziv},
        'Trening': {'tip': termin['Trening'].tip, 'idtrening': termin['Trening'].idtre},
        'IdDrzi': {'idkor': {'mejl': termin['IdDrzi'].idkor.mejl}},
        'Pocetak': termin['Pocetak'],
        'Kraj': termin['Kraj'],
        'Preostalo': termin['Preostalo'],
        'Id': termin['IdTer']
    } for termin in termini]

    return JsonResponse({'termini': termini_data})


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def urediPaketPregled(request):
    '''
    Data funkcija dohvata stranicu na kojoj su izlistani svi paketi i cekiranjem 1 paketa se odlazi na novu_formu gde se uredjuje paket
    :param request: Zahtev prosledjen serveru
    :return: varca html stranicu admin_urediPaket
    '''
    paketi = sviPaketi()
    context = {
        'paketi': paketi
    }
    return render(request, "proj/admin_urediPaket.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def adminPocetna(request):
    '''
    Data funkcija dohvata pocetnu stranicu vezanu za admina, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admina
    '''
    paketi = sviPaketi()
    context = {
        'paketi': paketi
    }
    return render(request, "proj/admin.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('trener')
def trenerPocetna(request):
    '''
    Data funkcija dohvata pocetnu stranicu za trenera, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu trener_glavna
    '''
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)
    sale = dohvati_sale()
    termini = sviTermini()
    slika = base64.b64encode(korisnik.slika).decode()
    sale_i_treninzi = []
    for sala in sale:
        treninzi = Trening.objects.filter(podrzava__idsala=sala)
#        print("treninzi")
#        print(treninzi)
        sale_i_treninzi.append({
            'sala': sala,
            'treninzi': treninzi
        })
    print(sale_i_treninzi)
    html = []
    for i in range(len(sale_i_treninzi)):
        tipovi = []
        for trening in sale_i_treninzi[i]['treninzi']:
            tipovi.append(trening.tip)
        html.append((sale_i_treninzi[i]['sala'], tipovi))
    # id_kor = korisnik.idkor
    day_list = ['PON', 'UTO', 'SRE', 'CET', 'PET', 'SUB', 'NED']
    context = {
        "sale_i_treninzi": html,
        "korisnik": korisnik,
        "slika": slika,
        "termini": termini,
        "dani": day_list
    }
    return render(request, "proj/trener_glavna.html", context)


# David Duric 2021/0102
def registracija(request):
    '''
    Funkcija samo prosledjuje stranicu za registraciju klijentu.
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu za registraciju
    '''
    return render(request, "proj/registracija.html")


# David Duric 2021/0102
# Ova funkcija cuva kredencijal lozinke u redisu, a korisnicki mejl u kolacicu, dok na taj mejl salje kod
# Ukoliko korisnik vec postoji, vraca se greska
def registrujSe(request):
    '''
    Funkcija koja prima potencijalno korisnicko ime i lozinku i cuva ih u redisu uz kod koji salje na mejl, a koji
    sluzi za proveru ispravnosti mejla.
    :param request: Zahtev prosledjen serveru
    :return: funkcija nema povratnu vrednost
    '''
    korisnickiMejl = request.POST.get('username')
    korisnickaLozinka = request.POST.get('password')
#    print(korisnickiMejl)
#    print(korisnickaLozinka)
    if korisnikPostoji(korisnickiMejl):
        return render(request, "proj/registracija.html", {'porukaGreske': True})
    with Redis(host='localhost', port='6379') as redis:
        if not redis.setnx(korisnickiMejl, 1):
            return render(request, "proj/registracija.html", {'porukaGreske': True})
        redis.expire(korisnickiMejl, 120)
        randomnum = random.randint(10000, 99999)
        code_mail(korisnickiMejl, randomnum)
        credentials = f'{korisnickiMejl}:{randomnum}'
#        print(credentials)
        redis.set(credentials, korisnickaLozinka, ex=120)
        response = render(request, "proj/registracija.html", {'show_popup': True})
        response.set_cookie('username', korisnickiMejl, max_age=600)
        return response


# David Duric
# Ova funkcija iz zahtjeva izvlaci korisnicko ime i kod i provjerava da li postoji takav zahtjev
# Ako se u redisu pronadje lozinka, dodaje se u bazu korisnik sa zadatim korisnickim imenom i lozinkom
# Inace se zahtjev odbija
def potvrdaKoda(request):
    '''
    Funkcija prima kod i uporedjuje ga sa onim sto je u redis bazi. U slucaju jednakosti kredencijali korisnika se
    perzistiraju u bazu, u protivnom se zahtjev brise. Nakon cega je potrebna ponovna registracija.
    :param request: Zahtev prosledjen serveru
    :return: Odgovarajuva stranica i odgovarajuca poruka, zavisno od ishoda.
    '''
    if request.method == 'POST':
        auth_code = int(json.loads(request.body).get('authCode'))
        korisnickiMejl = request.COOKIES.get('username')
        with Redis(host='localhost', port='6379') as redis:
            redis.delete(korisnickiMejl)
            korisnickaLozinka = redis.getdel(f'{korisnickiMejl}:{auth_code}')
            if korisnickaLozinka is None:
                return JsonResponse({'success': False})
        registracija_korisnika(korisnickiMejl, korisnickaLozinka.decode())
        response = JsonResponse({'success': True})
        response.delete_cookie('username')
        return response

    return JsonResponse({'success': False})


# David Duric 2021/0102
# ova funkcija ce da uradi login korisnika
def login_user(request):
    '''
    Funkcija omogucava korisniku pristup njegovom nalogu nakon uspesne autentikacije ili ispisuje odgovarajucu poruku u
    suprotnom.
    :param request: Zahtev prosledjen serveru
    :return: Povratna vrednost je stranica na koju se korisnik prebacuje, zavisno od uspesnosti operacije. Moze biti vracena
    html stranica ili se zahtev preusmerava.
    '''
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        try:
            korisnik = Korisnik.objects.get(mejl=username)
            user = User.objects.get(username=username)
        except:
            return render(request, 'proj/pocetna.html', {'greska': True, 'porukaGreske': "Korisničko ime ne postoji."})
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session.set_expiry(1500)
            if korisnik.uloga == 'trener':
                return redirect('trenerPocetna')
            if korisnik.uloga == 'clan':
                return redirect('korisnikPocetna')
            return redirect('adminPocetna')
        return render(request, 'proj/pocetna.html', {'greska': True, 'porukaGreske': 'Lozinka nije ispravna!'})


# David Duric 2021/0102
# Dohvata login stranicu
def go_to_login(request):
    '''
    Dohvata login stranicu.
    :param request: Zahtev prosledjen serveru
    :return: Login stranica
    '''
    return render(request, 'proj/pocetna.html')


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('admin')
def dodavanjePaketa(request):
    '''
    Data funkcija uz pomoc POST zahteva uzima podatke iz forme vezane za pakete,a
    zatim dodaje dati paket u bazu podataka, uz pomoc funkcije dodajPaket
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_dodajPaket
    '''
    imePaketa = request.POST.get("nazivPaketa")
    brojTermina = request.POST.get("brojTermina")
    brojDana = request.POST.get("brojDana")
    cena = request.POST.get("cenaPaketa")
    listaTreninga = sviTreninzi()
    treninzi = []

    for i in range(0, len(listaTreninga)):
        if "item" + str(i + 1) in request.POST:
            treninzi.append(listaTreninga[i]['Tip'])

    provera = dodajPaket(imePaketa, cena, brojTermina, brojDana, treninzi)
    context = {
        'provera': provera
    }
    return render(request, "proj/admin_dodajPaket.html", context)


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('admin')
def dodajPaketPregled(request):
    '''
    Data funkcija dohvata stranicu admin_dodajPaket, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_dodajPaket
    '''
    treninzi = sviTreninzi();
    print("treninzi")
    print(treninzi)
    context = {
        'treninzi': treninzi,

        'provera': 3

    }
    return render(request, "proj/admin_dodajPaket.html", context)


# Sofija Martinovic 0486/2021
@login_required(login_url='login')
@role_required('admin')
def dodajTreneraPregled(request):
    '''
    Data funkcija dohvata html stranicu, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_dodajTrenera
    '''
    treninzi = sviTreninzi()
    print("treninzi")
    print(treninzi)
    context = {
        'treninzi': treninzi,
        'provera': 3
    }
    return render(request, "proj/admin_dodajTrenera.html", context)


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('admin')
def dodavanjeTrenera(request):
    '''
    Data funkcija dohvata podatke iz forme vezane za trenera, uz pomoc POST metode,
    a zatim uz pomoc funkcije dodaj_trenera, dodaje trenera u bazu podataka
    :param request: Zahtev prosledjen serveru
    :return: varaca html stranicu dodajTrenera
    '''
    ime = request.POST.get("username")
    lozinka = request.POST.get("password")
    listaTreninga = sviTreninzi()
    treninzi = []
    for i in range(0, len(listaTreninga)):
        if "item" + str(i + 1) in request.POST:
            treninzi.append(listaTreninga[i]['Tip'])
    if 'image' in request.FILES:
        slika = request.FILES['image']  # TODO dodati sliku
#    print(treninzi)
    for i in range(0, len(treninzi)):
        print(treninzi[i])
        treninzi[i] = dohvatanje_id_treninga(treninzi[i])

 #   print(treninzi)
    provera = dodaj_trenera(ime, lozinka, treninzi, slika)
    if provera == 0:
        user = User.objects.create_user(username=ime, password=lozinka)
        user.save()

    context = {
        "provera": provera
    }
    return render(request, "proj/admin_dodajTrenera.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def dodajTreningPregled(request):
    '''
    Data funkcija dohvata html stranicu admin_dodajTrening, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_dodajTrening
    '''
    return render(request, "proj/admin_dodajTrening.html", {"provera": 3})


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def dodavanjeTreninga(request):
    '''
    Data funkcija uz pomoc POST metode dohvata podatke iz forme i ubacuje trening u bazu podataka,
    uz pomoc metode dodajTrening()
    :param request:
    :return:
    '''
    nazivTreninga = request.POST.get("tip_treninga")
#    print("TRENING")
#    print(nazivTreninga)
    provera = dodajTrening(nazivTreninga)
    context = {
        "provera": provera
    }
    return render(request, "proj/admin_dodajTrening.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def odobriKomentarPregled(request):
    '''
    Data funkcija dohvata html stranicu admin_komentari, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_komentari
    '''
    komentari = dohvatiNeodobreneKomentare()
    context = {
        "komentari": komentari
    }
    return render(request, "proj/admin_komentari.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def odobravanjeKomentara(request):
    '''
    Data funkcija uz pomoc POST metode dohvata podatke, a zatim gleda da li su komentari odobreni ili ne,
    jer u slucaju da nisu odobreni se brisu iz baze, a onaj komentar koji se cekira u formi se ubacuje u bazu
     i dobija vrednost statusa 1
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_komentari
    '''
    komentari = dohvatiNeodobreneKomentare()
    komentariZaOdobravanje = []
    komentariZaBrisanje = []
    for i in range(0, len(komentari)):
        if "item" + str(komentari[i].idkom) in request.POST:
            komentariZaOdobravanje.append(komentari[i])

    for i in range(0, len(komentari)):
        if (komentari[i] not in komentariZaOdobravanje):
            komentariZaBrisanje.append(komentari[i])
#    print(komentariZaBrisanje)
    if (len(komentariZaBrisanje) + len(komentariZaOdobravanje) != len(komentari)):
        print("GRESKA!")

    for komentar in komentariZaOdobravanje:
        odobriKomentar(komentar.idkom)
    for komentar in komentariZaBrisanje:
        obrisiKomentar(komentar.idkom)

    return render(request, "proj/admin_komentari.html")


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('admin')
def urediTrenera(request):
    '''
    Data funkcija dohvata html stranicu admin_urediTrenera, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_urediTrenera
    '''
    treneri = dohvatiSveTrenere()
    context = {
        'treneri': treneri
    }
    return render(request, "proj/admin_urediTrenera.html", context)


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('admin')
def novaFormaPregled(request, paket_id):
    '''
    Data funkcija dohvata html stranicu nova_forma, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :param id: Zahtev prosledjen serveru
    :return: vraca html stranicu nova_forma
    '''
    treninzi = dohvatiStaNeObuhvata(dohvatiPaketPoId(paket_id).naziv)
    for trening in treninzi:
        print(trening.tip)

 #   print(treninzi)

  #  print(dohvatiPaketPoId(paket_id).naziv)
    context = {
        "treninzi": treninzi,
        "paket_id": paket_id,
        "paket": dohvatiPaketPoId(paket_id)
    }
    return render(request, "proj/nova_forma.html", context)


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('admin')
def novaForma(request):
    '''
    Data funkcija uz pomoc POST metode uzima podatke iz forme, a zatim poziva funkciju urediPaket i na taj nacin
    azurira podatke u bazi za taj paket
    :param request: Zahtev prosledjen serveru
    :param id: Zahtev prosledjen serveru
    :return: vraca html stranicu nova_forma
    '''
    idP = request.POST.get("paket_id")
#    print(request.POST)
    paket = dohvatiOdgovarajuciPaket(idP)
#    print(paket.idpak)
    br_termina = request.POST.get("br_termina")
    br_dana = request.POST.get("br_dana")
    cena = request.POST.get("cena")
    naziv_paketa = request.POST.get("naziv_paket")
    treninzi = sviTreninzi()
    lTrening = []
    for trening in treninzi:
        print(trening)
        lTrening.append(trening['Tip'])
#    print(lTrening)
    lista = []
    for trening in lTrening:
        if trening in request.POST:
            lista.append(trening)

    urediPaket(paket.naziv, br_termina, br_dana, cena, naziv_paketa, lista)

    return redirect('/adminPocetna')


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('admin')
def uredjivanjePregled(request):
    '''
    Data funkcija dohvata html stranicu uredjivanje_trenera, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu uredjivanje_trenera
    '''
    treninzi = sviTreninzi();
#    print("treninzi")
#    print(treninzi)
    context = {
        'treninzi': treninzi
    }
    return render(request, "proj/uredjivanje_trenera.html", context)


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('admin')
def uredjivanje(request, id_tr):
    '''
    Data funkcija dohvata promene vezane za datakog trenera i menja podatke u bazi,
    uz pomoc funkcije uredi_trenera
    :param request: Zahtev prosledjen serveru
    :param id: Zahtev prosledjen serveru
    :return: vraca html stranicu uredjivanje_trenera
    '''
    treninzi = sviTreninziKojeTrenerNeDrzi(id_tr)
    trenutniTrener = dohvatiOdgovarajucegTrenera(id_tr)
    print("treninzi")
    print(treninzi)
    context = {
        'treninzi': treninzi,
        'trener': trenutniTrener
    }
    #   uredi_trenera(id,treninzi)
    return render(request, "proj/uredjivanje_trenera.html", context)


# Sofija Martinovic, 0486/2021
# David Duric, 0102/2021
@login_required(login_url='login')
@role_required('trener')
def dodavanjeTermina(request):
    '''
    Data funkcija uz pomoc POST metode dohvata podatke iz forme, a zatim poziva funkciju dodajTermin,
    koja vrsi dodavanje termina u bazu podataka od strane ulogovanog trenera
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu trener_dodajaTermin
    '''
    print("DODAVANJE TERMINA")
    username = request.user.username
    korisnik = Korisnik.objects.get(mejl=username)
    trener_id = korisnik.idkor
    sala = request.POST.get("sale")
    sala = int(sala)
    print(sala)
    dan = request.POST.get("dan")
    match dan:
        case "Ponedeljak":
            dan = "PON"
        case "Utorak":
            dan = "UTO"
        case "Sreda":
            dan = "SRE"
        case "Cetvrtak":
            dan = "CET"
        case "Petak":
            dan = "PET"
        case "Subota":
            dan = "SUB"
        case "Nedelja":
            dan = "NED"

 #   print(dan)

    broj = int(request.POST.get("slobodnih"))
 #   print(broj)
    if broj <= 0:
        return dodajTerminRedirect(request, 'Broj mesta mora da bude pozitivan broj!')
    vreme_od = datetime.strptime(request.POST.get("timeStart"), "%H:%M").time()
 #   print(vreme_od)
    vreme_do = datetime.strptime(request.POST.get("timeEnd"), "%H:%M").time()
 #   print(vreme_do)
    if (vreme_do < time(8, 0) or vreme_do > time(22, 0) or
        vreme_od < time(8, 0) or vreme_do > time(22, 0)) or vreme_do < vreme_od:
        return dodajTerminRedirect(request, 'Neodgovarajuca vremena pocetka i kraja')
 #   print("LISTA")
    tip_treninga = request.POST.get('radio')
 #   print(tip_treninga)
    zauzeto = Termin.objects.filter(dan=dan)
    for z in zauzeto:
        if z.idpodrzava.idsala_id != sala and z.iddrzi.idkor.idkor != trener_id:
            continue
        if z.pocetak < vreme_od and z.kraj > vreme_od:
            print(1111)
            return dodajTerminRedirect(request, 'Sala je zauzeta u zadatom terminu ili ste Vi zauzeti.')
        if z.pocetak < vreme_do and z.kraj > vreme_do:
            print(2222)
            return dodajTerminRedirect(request, 'Sala je zauzeta u zadatom terminu ili ste Vi zauzeti.')
        if z.pocetak >= vreme_od and z.kraj <= vreme_do:
            print(3333)
            return dodajTerminRedirect(request, 'Sala je zauzeta u zadatom terminu ili ste Vi zauzeti.')
        if z.pocetak <= vreme_od and z.kraj >= vreme_do:
            print(4444)
            return dodajTerminRedirect(request, 'Sala je zauzeta u zadatom terminu ili ste Vi zauzeti.')

    podrzavanja = Podrzava.objects.filter(idsala_id=sala, idtre2__tip=tip_treninga)
    if not podrzavanja:
        return dodajTerminRedirect(request, 'Ova sala ne podrzava zadati trening')

    dodajTermin(trener_id, tip_treninga, sala, dan, vreme_od, vreme_do, broj)

    return redirect('/trenerPocetna')


# Sofija Martinovic, 0486/2021
@login_required(login_url='login')
@role_required('trener')
def dodajTerminPregled(request):
    '''
    Data funkcija dohvata html stranicu trener_dodajaTermin, uz pomoc GET metode
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu trener_dodajaTermin
    '''

    sala = dohvati_sale()
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)
    id_kor = korisnik.idkor
    treninzi = drzi_treninge(id_kor)
#    print("Treninzi:", treninzi)
#    print("Sale:", sala)
#    print("Korisnik ID:", id_kor)
    context = {
        'korisnik': korisnik,
        'treninzi': treninzi,
        'sale': sala,
        'id_kor': str(id_kor),
        'poruka': 'Popunite formu'
    }
    return render(request, "proj/trener_dodajaTermin.html", context)


def dodajTerminRedirect(request, poruka):
    sala = dohvati_sale()
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)
    id_kor = korisnik.idkor
    treninzi = drzi_treninge(id_kor)
#    print("Treninzi:", treninzi)
#    print("Sale:", sala)
#    print("Korisnik ID:", id_kor)
    context = {
        'korisnik': korisnik,
        'treninzi': treninzi,
        'sale': sala,
        'id_kor': str(id_kor),
        'poruka': poruka
    }
    return render(request, "proj/trener_dodajaTermin.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('admin')
def primeniPromeneNadTrenerom(request):
    '''
    Data funkcija uz pomoc POST metode uzima podatke o treneru iz forme i za datog trenera(id),
    vrsi promene u bazi uz pomoc funkcije uredi_trenera
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu adminPOcetna
    '''
    slika = None
    trener = request.POST.get("trener_id")
    if 'image' in request.FILES:
        slika = request.FILES['image']
        # slika = base64.b64encode(slika).decode()
    sviTr = sviTreninzi()
    noviTreninzi = []
    for i in range(0, len(sviTr)):
        if "item" + str(i + 1) in request.POST:
            noviTreninzi.append(sviTr[i]['idtre'])

    uredi_trenera(trener, noviTreninzi, slika)
    paketi = sviPaketi()
    context = {
        "paketi": paketi
    }
    return redirect('/adminPocetna')


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('clan')
def paketiKorisnikaOdabranPaket(request):
    '''
    Data funkcija uz pomoc POST metode iz forme izvlaci naziv paketa i uz pomoc funkcije odajPretplatuAkoNePostoji,
    clanu teretane  se salje obavestenje da aktivna pretplata postoji, a u suprotnom poziva se funkcija oslobodiTermine,
    koja clana teretane obavestava da je se uspesno pretplatio na zadati paket
    :param request: Zahtev prosledjen serveru
    :return: vraca poruku datom clanu da li se uspesno pretplatio na paket
    ili da li postoji vec neka pretplata za datog clana
    '''
    if request.method == "POST":
        paket_naziv = json.loads(request.body).get('paket_naziv')
        username = request.user.username
 #       print(username)

        if dodajPretplatuAkoNePostoji(username, paket_naziv) == -1:
            message = 'Aktivna pretplata jos uvek postoji'
            success = False
        else:
            proj.models.oslobodiTermine(username, paket_naziv)
            message = f'Uspesno ste pretplaceni na paket {paket_naziv}'
            success = True
        print(request.POST)

        return JsonResponse({"message": message, "success": success})


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('trener')
def trenerPregledTreninga(request):
    '''
    Data funkcija uz pomoc GET metode dohvata podatke o treninzima za datog trenera
    :param request: Zahtev se salje serveru
    :return: vraca html stranicu trener_treninzi
    '''
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)

    termini = sviTermini()
    slika = base64.b64encode(korisnik.slika).decode()
    # id_kor = korisnik.idkor
    day_list = ['PON', 'UTO', 'SRE', 'CET', 'PET', 'SUB', 'NED']
    context = {
        "korisnik": korisnik,
        "slika": slika,
        "termini": termini,
        "dani": day_list
    }
    return render(request, "proj/trener_treninzi.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('clan')
def korisnikPregledTreninga(request):
    '''
    Data funkcija uz pomoc GET metode dohvata treninge vezane za clana teretane
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu korisnik_treninzi
    '''
    username = request.user.username
    korisnik = get_object_or_404(Korisnik, mejl=username)

    termini = licniRaspored(korisnik.idkor, "clan")

 #   print(termini)

    # id_kor = korisnik.idkor
    day_list = ['PON', 'UTO', 'SRE', 'CET', 'PET', 'SUB', 'NED']
    context = {
        "korisnik": korisnik,

        "termini": termini,
        "dani": day_list
    }
    return render(request, "proj/korisnik_treninzi.html", context)


# David Duric 2021/0102
@login_required(login_url='login')
@role_required('clan')
def dodajMeUTermin(request):
    '''
    Data funkcija dodaje u termin korisnika, ako ima mesta i u zavisnoti od toga clanu teretane
    se salje odgovarajuca poruka
    :param request: Zahtev prosledjen serveru
    :return: vraca se poruka korisniku
    '''
    idter = int(json.loads(request.body).get('idter'))
#    print(idter)
    user = request.user.username
    korisnik = Korisnik.objects.get(mejl=user)
    message = None
    success = False
    if proj.models.ImaAktivnuPretplatu(user):
        ret = prijaviTermin(korisnik.idkor, idter)
        if ret == 0:
            message = "Uspesno ste prijavljeni na termin!"
            success = True
        elif ret == -1:
            message = "Nema slobodnih mesta za prijavu!"
        elif ret == -2:
            message = "Vasa pretplata ne pokriva ovaj tip treninga"
        elif ret == -3:
            message = "Pratite zadati termin. Nije dozvoljeno pratiti isti termin dvaput"
    else:
        message = 'Nemate aktivnu pretplatu'
    print(message)
    workouts = licniRaspored(korisnik.idkor, korisnik.uloga)
    print(workouts)
    return JsonResponse({"message": message, "success": success})


# David Duric, 0102/2021
def logout_user(request):
    '''
    Data funkcija radi logout korisnika, koji se uspesno prijavio
    :param request: Zahtev prosledjen serveru
    :return: povratna vrednost je stranica na koju se korisnik prebacuje
    '''
    logout(request)
    return redirect('index')


# David Duric, 0102/2021
@login_required(login_url='login')
@role_required('clan')
def izbaciMeIzTermina(request):
    '''
    Data funkcija izbacuje zadatog korisnika iz termina, a promena u bazi se vidi uz pomoc funkcije odjaviTermin
    :param request: Zahtev prosledjen serveru
    :return: vraca poruku korisniku da je termin odjavljen, kao i uspesnost zadate operacije
    '''
    idter = int(json.loads(request.body).get('idter'))
    print(idter)
    user = request.user.username
    korisnik = Korisnik.objects.get(mejl=user)
    odjaviTermin(korisnik.idkor, idter)
    return JsonResponse({"message": "Termin odjavljen", "success": True})


# David Duric, 0102.2021
@role_required('trener')
def ukloniMojTermin(request):
    '''
    Data funkcija uklanja termin korisnika, a promena u bazi se vidi uz pomoc funkcije ukloniTermin
    :param request: Zahtev prosledjen serveru
    :return: vraca poruku korisniku da je termin odjavljen, kao i uspesnost zadate operacije
    '''
    idter = int(json.loads(request.body).get('idter'))
    print(idter)
    user = request.user.username
    korisnik = Korisnik.objects.get(mejl=user)
    ukloniTermin(korisnik.idkor, idter)
    return JsonResponse({"message": "Termin odjavljen", "success": True})


# Kristina Kragovic, 0270/2021
def gostPocetna(request):
    '''
    Data funkcija uz pomoc GET metode dohvata stranicu gost_glavna
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu gost_glavna
    '''

    sale = dohvati_sale()
    termini = sviTermini()
    sale_i_treninzi = []
    for sala in sale:
        treninzi = Trening.objects.filter(podrzava__idsala=sala)
        print("treninzi")
        print(treninzi)
        sale_i_treninzi.append({
            'sala': sala,
            'treninzi': treninzi
        })
    print(sale_i_treninzi)
    html = []
    for i in range(len(sale_i_treninzi)):
        tipovi = []
        for trening in sale_i_treninzi[i]['treninzi']:
            tipovi.append(trening.tip)
        html.append((sale_i_treninzi[i]['sala'], tipovi))
    # id_kor = korisnik.idkor
    day_list = ['PON', 'UTO', 'SRE', 'CET', 'PET', 'SUB', 'NED']
    context = {
        "sale_i_treninzi": html,
        "termini": termini,
        "dani": day_list
    }
    return render(request, "proj/gost_glavna.html", context)


# Kristina Kragovic, 0270/2021
def gostKomentar(request):
    '''
    Data funkcija uz pomoc GET metode dohvata stranicu sa komentarima koje je dao gost o trenerima i teretani
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu gost_o_nama
    '''
    sviKorisnici = dohvatiSveTrenere()
    sviKomentari = dohvatiKomentareOTeretani()

    context = {
        'treneri': sviKorisnici,
        'komentari': sviKomentari
    }
    # print(sviKorisnici)
    return render(request, "proj/gost_o_nama.html", context)


# Kristina Kragovic, 0270/2021
@login_required(login_url='login')
@role_required('clan')
def ostaviKomentar(request):
    '''
    Data funkcija uz pomoc POST metode dohvata podatke iz forme vezane za komentare od strane korisnika, a zatim
    dati komentar koji je dao korisnik se unosi u bazu uz pomoc funkcije kreiraj_komentar
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu korisnik_komentarisi
    '''
    if request.method == "POST":
        tekst = request.POST.get('komentar')
        trener_id = request.POST.get('trener')
        print("TRNER ID: " + trener_id)
        if trener_id == "teretana":
            trener_id = None
        else:
            trener_id = int(trener_id)
        user = request.user.username
        k = Korisnik.objects.get(mejl=user)

        kreiraj_komentar(tekst=tekst, trener_id=trener_id, idautor=k.idkor)
    user = request.user.username
    korisnik = Korisnik.objects.get(mejl=user)
    pracenja = Prati.objects.filter(idkor=korisnik.idkor)
    treneri_ids = set()
    for pracenje in pracenja:
        treneri_ids.add(pracenje.idter.iddrzi.idkor.idkor)

    treneri = Korisnik.objects.filter(idkor__in=treneri_ids, uloga='trener')
    return render(request, 'proj/korisnik_komentarisi.html', {'treneri': treneri, 'korisnik': korisnik})


# David Duric, 0102/2021
@login_required(login_url='login')
@role_required('trener')
def pregledPrisutnih(request):
    '''
    Data funkcija uz pomoc POST metode dohvata id trenera iz forme,
    a zatim trener vrsi pregled prisutnih clanova za zadati termin i promene upisuje u bazu uz pomoc funkcije
    pratiOdredjeniTermin
    :param request: Zahtev prosledjen serveru
    :return: u slucaju uspeha vraca stranicu trener_evidencija, a u suprotnom baca izuzetak i vraca neka_druga_stranica
    '''

    if request.method == 'POST':

        username = request.user.username
        korisnik = get_object_or_404(Korisnik, mejl=username)
        idter = int(request.POST.get('idter'))
        pratiOdgovarajuciTermin = pratiOdredjenTermin(idter)
        korisniciPretplate = []
#        print("KO IMA PRETPLATU")
        for prati in pratiOdgovarajuciTermin:
            korisniciPretplate.append(ImaAktivnuPretplatu(prati.idkor.mejl))
            print(prati.idkor.mejl, ImaAktivnuPretplatu(prati.idkor.mejl))
        parovi = list(zip(pratiOdgovarajuciTermin, korisniciPretplate))
        context = {
            "korisnik": korisnik,
            "id_termina": idter,
            "parovi": parovi
        }
        return render(request, "proj/trener_evidencija.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('trener')
def potvrdiPrisutne(request):
    '''
    Data funkcija uz pomoc POST metode uzima podatke iz forme za potvrdu prisutnosti datom terminu,
    a zatim se vrsi pretplata datog za odredjeni termin (u bazi se vide sve pretplate za odgovarajuceg korisnika)
    ili se vrsi provera da li prati odgovarajuci termin.Sve promene u bazi se azuriraju uz pomoc funkcija
    pretplateOdredjenogKorisnika(korisnik) i pratiOdredjenTermin(idter)
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu trener_evidencija
    '''
    if request.method == 'POST':
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)
        id_termina = data.pop("id_termina", None)
        pritisnuto_dugme = data.pop("clicked_button", None)
#        print(pritisnuto_dugme)
        selected_ids = list(data.keys())

        for korisnik in selected_ids:
            pretplata = pretplateOdredjenogKorisnika(korisnik)
            pretplata.preostalotermina = pretplata.preostalotermina - 1;
            if pretplata.preostalotermina == 0:
                send_new_email([dohvatiKorisnikaPoId(korisnik).mejl], 'Potroseni termini',
                               "Obaveštavamo Vas da ste potrošili sve termine. Vaš Step By Step")
            pretplata.save()
        idter = id_termina[0]
        pratiOdgovarajuciTermin = pratiOdredjenTermin(idter)
        username = request.user.username
        korisnik = get_object_or_404(Korisnik, mejl=username)
        korisniciPretplate = []
        for prati in pratiOdgovarajuciTermin:
            korisniciPretplate.append(ImaAktivnuPretplatu(prati.idkor.mejl))
        parovi = list(zip(pratiOdgovarajuciTermin, korisniciPretplate))
        context = {
            "korisnik": korisnik,
            "id_termina": idter,
            "parovi": parovi
        }
        return render(request, "proj/trener_evidencija.html", context)


# Aleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('trener')
def izbacivanjeSaTermina(request):
    '''
    Data  funkcija uz pomoc POST metode dohvata podatke iz forme vezane za izbacivanje korisnika sa termina.
    Takodje, data funkcija prati koliko je izostajao dati korisnik i ukoliko je previse izostajao sa termina,
    korisniku se salje automatski mejl da je izbacen sa termina zbog izostajanja. U suprotnom ukoliko je bio redovan,
    za korisnika se prati koliko mu je jos ostalo termina.
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu trener_evidencija
    '''
    if request.method == 'POST':
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)
        termin = data.pop("id_termina", None)
        pritisnuto_dugme = data.pop("clicked_button", None)
        korisnik = data.pop("id_korisnika", None)
        korisnik = korisnik[0]
#        print("HEJ")
#        print(data)
#        print(korisnik)
        termin = termin[0]
        # selected_ids = list(data.keys())
        pratiObrisiKorisnika(korisnik, termin)
        terminObjekat = dohvatiTerminPoId(termin)
        send_new_email([dohvatiKorisnikaPoId(korisnik).mejl], "StepByStep - obavestenje",
                       f"Izbaceni ste sa termina: {terminObjekat.dan} {terminObjekat.pocetak} zbog izostajanja")
        pratiOdgovarajuciTermin = pratiOdredjenTermin(termin)
        odgovarajuciTermin = dohvatiTerminPoId(termin)
        odgovarajuciTermin.preostalo = odgovarajuciTermin.preostalo + 1
        odgovarajuciTermin.save()
        username = request.user.username
        korisnik = get_object_or_404(Korisnik, mejl=username)
        korisniciPretplate = []
        for prati in pratiOdgovarajuciTermin:
            korisniciPretplate.append(ImaAktivnuPretplatu(prati.idkor.mejl))
        parovi = list(zip(pratiOdgovarajuciTermin, korisniciPretplate))

        context = {
            "korisnik": korisnik,
            "id_termina": termin,
            "parovi": parovi
        }
        return render(request, "proj/trener_evidencija.html", context)


# Kristina Kragovic, 0270/2021
@login_required(login_url='login')
@role_required('admin')
def ukloniPaketPrimeni(request):
    '''
    Data funkcija uz pomoc POST metode dohvata paket koji se uklanja i promena u bazi se vidi uz pomoc funkcije
    obrisiPaket, koja brise paket koji smo oznacili u formi
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu adminPocetna
    '''
    data = request.POST.copy()
    naziv_paketa = data.pop("paket")
    naziv_paketa = naziv_paketa[0]
    obrisiPaket(naziv_paketa)
    return redirect('/adminPocetna')


# Kristina Kragovic, 0270/2021
@login_required(login_url='login')
@role_required('admin')
def ukloniTreneraPrimeni(request):
    '''
    Data funkcija uz pomoc POST metode dohvata trenera koji se uklanja i promena u bazi se vidi uz pomoc funkcije
    ukloni_trenera, koja brise trenera koga smo oznacili u formi
    :param request: Zahtev prosledjen serveru
    :return: vraca html stranicu admin_ukloniTrenera
    '''
#    print(request.POST)
    trener_id = request.POST.get('trener_id')
    trener_id = trener_id
#    print(trener_id)
#    print("TRENEEEEEEEEER")
    ukloni_trenera(trener_id)
    treneri = dohvatiSveTrenere()
    context = {
        'treneri': treneri
    }
    return redirect('/adminPocetna')


# KAleksandar Ilic, 0495/2021
@login_required(login_url='login')
@role_required('trener')
def izmenaPonudeTreninga(request):
    '''
    Data funkcija vrsi promenu treninga na zahtev zadatog trenera
    :param request: Zahtev prosledjen serveru
    :return: nema
    '''
    idSale = int(json.loads(request.body).get('idsale'))
#    print(idSale)
    korisnik = Korisnik.objects.get(mejl=request.user.username)
    treninzi = drzi_treninge(korisnik.idkor)
    podrzavanja = Podrzava.objects.filter(idsala_id=idSale)
#    print(treninzi)
    set_podrzava = []
    for pod in podrzavanja:
        podrzaniTrening = {
            'Tip': pod.idtre2.tip,
            'idtre': pod.idtre2.idtre
        }
        set_podrzava.append(podrzaniTrening)
    presek = [value for value in treninzi if value in set_podrzava]
 #   print(set_podrzava)
 #   print(presek)
