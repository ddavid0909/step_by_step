import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.utils.crypto import get_random_string
from django.db import IntegrityError

from proj.mail import send_new_email


# Create your models here.
class Drzi(models.Model):
    iddrzi = models.AutoField(db_column='IdDrzi', primary_key=True)  # Field name made lowercase.
    idkor = models.ForeignKey('Korisnik', models.CASCADE, db_column='IdKor')  # Field name made lowercase.
    idtre1 = models.ForeignKey('Trening', models.CASCADE, db_column='IdTre1')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Drzi'
        unique_together = (('idkor', 'idtre1'),)


class Komentar(models.Model):
    idkom = models.AutoField(db_column='IdKom', primary_key=True)  # Field name made lowercase.
    tekst = models.CharField(db_column='Tekst', max_length=200)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    datum = models.DateTimeField(db_column='Datum')  # Field name made lowercase.
    idautor = models.ForeignKey('Korisnik', models.CASCADE, db_column='IdAutor', blank=True,
                                null=True)  # Field name made lowercase.
    idkomentarisan = models.ForeignKey('Korisnik', models.CASCADE, db_column='IdKomentarisan',
                                       related_name='komentar_idkomentarisan_set', null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Komentar'


class Korisnik(models.Model):
    idkor = models.AutoField(db_column='IdKor', primary_key=True)  # Field name made lowercase.
    mejl = models.CharField(db_column='Mejl', unique=True, max_length=45)  # Field name made lowercase.
    uloga = models.CharField(db_column='Uloga', max_length=45)  # Field name made lowercase.
    sifra = models.CharField(db_column='Sifra', max_length=45)  # Field name made lowercase.
    slika = models.BinaryField(db_column='Slika', blank=True, null=True)  # Field name made lowercase.

    def __json__(self):
        return {'idkor': self.idkor, 'mejl': self.mejl, 'uloga': self.uloga, 'sifra': self.sifra, 'slika': self.slika}

    class Meta:
        managed = True
        db_table = 'Korisnik'


class Obuhvata(models.Model):
    idobuh = models.AutoField(db_column='IdObuh', primary_key=True)  # Field name made lowercase.
    idtre = models.ForeignKey('Trening', models.CASCADE, db_column='IdTre')  # Field name made lowercase.
    idpak = models.ForeignKey('Paket', models.CASCADE, db_column='IdPak')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Obuhvata'
        unique_together = (('idtre', 'idpak'),)


class Paket(models.Model):
    idpak = models.AutoField(db_column='IdPak', primary_key=True)  # Field name made lowercase.
    brtermina = models.IntegerField(db_column='BrTermina')  # Field name made lowercase.
    dana = models.IntegerField(db_column='Dana')  # Field name made lowercase.
    cena = models.DecimalField(db_column='Cena', max_digits=10, decimal_places=2)  # Field name made lowercase.
    naziv = models.CharField(db_column='Naziv', max_length=40)  # Field name made lowercase.

    def __json__(self):
        return {
            'idpak': self.idpak,
            'Naziv': self.naziv,
            'Cena': float(self.cena),
            'Dana': self.dana,
            'BrTermina': self.brtermina
        }

    class Meta:
        managed = True
        db_table = 'Paket'


class Podrzava(models.Model):
    idpodrzava = models.AutoField(db_column='IdPodrzava', primary_key=True)  # Field name made lowercase.
    idsala = models.ForeignKey('Sala', models.CASCADE, db_column='IdSala')  # Field name made lowercase.
    idtre2 = models.ForeignKey('Trening', models.CASCADE, db_column='IdTre2')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Podrzava'
        unique_together = (('idsala', 'idtre2'),)


class Pokriva(models.Model):
    idpokriva = models.AutoField(db_column='IdPokriva', primary_key=True)  # Field name made lowercase.
    idpre = models.ForeignKey('Pretplata', models.CASCADE, db_column='IdPre')  # Field name made lowercase.
    idtre = models.ForeignKey('Trening', models.CASCADE, db_column='IdTre')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Pokriva'
        unique_together = (('idpre', 'idtre'),)


class Prati(models.Model):
    idprati = models.AutoField(db_column='IdPrati', primary_key=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Korisnik, models.CASCADE, db_column='IdKor')  # Field name made lowercase.
    idter = models.ForeignKey('Termin', models.CASCADE, db_column='IdTer')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Prati'
        unique_together = (('idkor', 'idter'),)


class Pretplata(models.Model):
    idpre = models.AutoField(db_column='IdPre', primary_key=True)  # Field name made lowercase.
    datumdo = models.DateTimeField(db_column='DatumDo')  # Field name made lowercase.
    preostalotermina = models.IntegerField(db_column='PreostaloTermina')  # Field name made lowercase.
    idpretplaceni = models.ForeignKey(Korisnik, models.CASCADE, db_column='IdPretplaceni')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Pretplata'


class Sala(models.Model):
    idsala = models.AutoField(db_column='IdSala', primary_key=True)  # Field name made lowercase.
    naziv = models.CharField(db_column='Naziv', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Sala'

    def __json__(self):
        return {
            "idsala": self.idsala,
            "naziv": self.naziv
        }


class Termin(models.Model):
    idter = models.AutoField(db_column='IdTer', primary_key=True)  # Field name made lowercase.
    dan = models.CharField(db_column='Dan', max_length=3)  # Field name made lowercase.
    pocetak = models.TimeField(db_column='Pocetak')  # Field name made lowercase.
    kraj = models.TimeField(db_column='Kraj')  # Field name made lowercase.
    idpodrzava = models.ForeignKey(Podrzava, models.CASCADE, db_column='IdPodrzava')  # Field name made lowercase.
    iddrzi = models.ForeignKey(Drzi, models.CASCADE, db_column='IdDrzi')  # Field name made lowercase.
    preostalo = models.IntegerField(db_column='Preostalo')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Termin'


class Trening(models.Model):
    idtre = models.AutoField(db_column='idTre', primary_key=True)  # Field name made lowercase.
    tip = models.CharField(db_column='Tip', max_length=45)  # Field name made lowercase.

    def __json__(self):
        return {'Tip': self.tip, 'idtre': self.idtre}

    class Meta:
        managed = True
        db_table = 'Trening'


# David Duric
def sviPaketi():
    '''
    SELECT * FROM PAKET
    ovaj upit dohvata sve informacije o paketima iz baze
    :return: povratna vrijednost je lista rijecnika, gdje svaki rijecnik predstavlja potrebne vrijednosti izvucene iz baze -
    naziv, cenu, brTermina, dane, kao i tipove treninga koje obuhvata
    '''
    paketi = Paket.objects.all()
    lista = []
    for elem in paketi:
        myDict = elem.__json__()
        obuhvatanja = Obuhvata.objects.filter(idpak=elem)
        obuhv = [o.idtre.tip for o in obuhvatanja]
        myDict['obuhvata'] = obuhv
        lista.append(myDict)
    return lista


# David Duric
def dodajPaket(naziv, cena, brtermina, dana, treninzi):
    '''
    Dodaje novi paket u bazu i azurira tabelu obuhvata sa potrebnim vezama paket-trening, ukoliko paket sa datim imenom vec ne postoji
    Argumenti funkcije su osnovne osobine paketa i nazivi treninga koji se dodaju.
    :param naziv: naziv paketa
    :param cena: cena paketa
    :param brtermina:  broj termina koji paket obuhvata
    :param dana: broj dana koji paket obuhvata
    :param treninzi: tipovi treninga koje paket obuhvata
    :return: Ukoliko paket vec postoji, vratice se vrednost -1. Ukoliko paket ne postoji, bice dodat u bazu i funkcija vraca 0
    '''
    try:
        paket = Paket.objects.get(naziv=naziv)
    except Paket.DoesNotExist:
        paket = None
    if paket != None:
        return -1
    noviObjekat = Paket(naziv=naziv, cena=cena,
                        brtermina=brtermina, dana=dana)
    noviObjekat.save()

    for nazivTreninga in treninzi:
        trening = Trening.objects.get(tip=nazivTreninga)
        obuhvata = Obuhvata(idpak=noviObjekat, idtre=trening)
        obuhvata.save()

    return 0


# David Durić
def obrisiPaket(naziv):
    '''
    DELETE FROM Paket WHERE naziv = @naziv
    Ova funkcija sluzi da obrise paket sa proslijedjenim nazivom
    :param naziv: naziv paketa
    :return: nema povratnu vrijednost. Garantuje da paket sa datim nazivom vise ne postoji
    '''
    Paket.objects.filter(naziv=naziv).delete()


# David Duric
def dohvatiNazivePaketa():
    '''
    Ova funkcija sluzi da izvuce nazive svih paketa koji postoje u bazi, potrebna za renderovanje stranice za
    uredjivanje paketa
    :return: funkcija vraca listu stringova koji su nazivi
    '''
    paketi = Paket.objects.all()
    lista = []
    for elem in paketi:
        lista.append(elem.naziv)
    return lista


# David Duric

def dohvatiStaNeObuhvata(naziv):
    '''
    Ova funkcija treba da vrati sve sto moze da se doda paketu od tipova treninga
    kao parametar prima naziv paketa koji mora da postoji zato sto ce tako biti napravljen korisnicki interfejs
    :param naziv: naziv paketa
    :return: vraca listu stringova koji su samo nazivi, a koji i treba da se prikazu na stranici
    '''
    idPaketa = Paket.objects.get(naziv=naziv)
    obuhvata = Obuhvata.objects.filter(idpak=idPaketa)
    ids = [elem.idtre.idtre for elem in obuhvata]
    neObuhvata = Trening.objects.exclude(idtre__in=ids)
    return neObuhvata


# David Duric
def urediPaket(naziv, brTermina=None, brDana=None, Cena=None, NazivPaketa=None, noviTreninzi=None):
    '''
    ova funkcija treba da izvrsi promene nad paketom na osnovu proslijedjenih vrijednosti
    :param naziv: naziv paketa
    :param brTermina: broj termina koji paket obuhvata
    :param brDana: broj dana koji paket obuhvata
    :param Cena: cena paketa
    :param NazivPaketa: novi naziv paketa
    :param noviTreninzi: novi tipovi treninga koje paket obuhvata
    :return: ukoliko se pokusa promena u ime koje je vec zauzeto - vraca se -1
    inace se promene perzistiraju u bazi i vraca se 0
    '''
    paket = Paket.objects.get(naziv=naziv)
    if NazivPaketa:
        try:
            paket1 = Paket.objects.get(naziv=NazivPaketa)
        except Paket.DoesNotExist:
            print("Paket dosad ne postoji")
            paket1 = None
        if paket1 and paket1.idpak != paket.idpak:
            print("Zauzeto ime")
            return -1
        paket.naziv = NazivPaketa
    if brTermina:
        paket.brtermina = brTermina
    if brDana:
        paket.dana = brDana
    if Cena:
        paket.cena = Cena
    if noviTreninzi:
        for nazivTreninga in noviTreninzi:
            try:
                trening = Trening.objects.get(tip=nazivTreninga)
            except Trening.DoesNotExist:
                print(f"Trening {nazivTreninga} ne postoji u bazi")
                continue
            obuhvata = Obuhvata(idpak=paket, idtre=trening)
            obuhvata.save()
    paket.save()


# David Duric
def dodajPretplatuAkoNePostoji(korisnicko_ime, naziv_paketa):
    '''
    Ova funkcija za zadatog korisnika dodaje novu pretplatu u slucaju da je najskorija pretplata istekla
    :param korisnicko_ime: korisnicko ime korisnika
    :param naziv_paketa: naziv paketa
    :return: ako je najskorija pretplata nije istekla, ova funkcija vraca -1 i ne mijenja bazu, a
    ukoliko jeste, azuriraju se kako tabela Pretplata tako i tabela Pokriva odgovarajucim podacima iz zadatog paketa
    '''

    # dohvati korisnika za zadatim imenom - ovo ce se uzimati iz logina tako da nije moguce da ne postoji
    k = Korisnik.objects.get(mejl=korisnicko_ime)
    # dohvati najskoriju pretplatu ovog korisnika
    zadnjaPretplata = Pretplata.objects.filter(idpretplaceni=k).aggregate(Max('datumdo'))
    danas = datetime.datetime.now(datetime.timezone.utc)
    print(danas)
    # ukolika pretplata nije istekla po danima
    if zadnjaPretplata['datumdo__max'] != None:

        if danas <= zadnjaPretplata['datumdo__max']:
            najnovijaPretplata = Pretplata.objects.filter(idpretplaceni=k, datumdo=zadnjaPretplata['datumdo__max'])[0]
            # provjeri da li je istekla po broju termina
            if najnovijaPretplata.preostalotermina > 0:
                # ako nije, ne dozvoli novu pretplatu
                print("Vec ste pretplaceni!")
                return -1
    print(zadnjaPretplata['datumdo__max'])
    paket = Paket.objects.get(naziv=naziv_paketa)
    datumdo = danas + datetime.timedelta(days=paket.dana)
    pretplata = Pretplata(datumdo=datumdo, preostalotermina=paket.brtermina, idpretplaceni=k)
    pretplata.save()
    treninzi = Obuhvata.objects.filter(idpak=paket)
    for trening in treninzi:
        pokriva = Pokriva(idpre=pretplata, idtre=trening.idtre)
        pokriva.save()
    return 0


# David Durić
def sviTreninzi():
    '''
    Ova metoda vraca sve tipove treninga koji su definisani u sistemu
    :return: Vraca listu recnika, a svaki recnik ima definisano polje Tip
    '''
    treninzi = Trening.objects.all()
    lista = []
    for elem in treninzi:
        lista.append(elem.__json__())
    return lista


# David Durić
def dodajTrening(tip):
    '''
    Ova metoda dodaje novi trening ukoliko je to moguce, odnosno ako trening vec ne postoji
    Ona garantuje da je nakon izvrsavanja taj tip u bazi, ali ne definise da li je vec bio tu ili je tek dodat.
    :param tip: tip treninga
    :return: vraca 0 u slucaju da se taj tip ne nalazi u bazi, a u suprotnom vraca -1
    '''

    try:
        trening = Trening.objects.get(tip=tip)
    except Trening.DoesNotExist:
        trening = Trening(tip=tip)
        trening.save()
        return 0
    return -1


# David Durić
def obrisiTrening(tip):
    '''
    Ova metoda brise trening iz sistema. Zajedno sa treningom se brisu svi podaci - koje pretplate su ih pokrivale i koji paketi obuhvatali.
    Garantuje se da nakon izvrsavanja ove funkcije u bazi nece biti tipa treninga, ali se ne definise da li je to slucaj jer ne postoji ili
    jer je obrisan
    :param tip: tip treninga
    :return: nema povratnu vrednost
    '''

    try:
        trening = Trening.objects.get(tip=tip)
        trening.delete()
    except:
        pass


# David Durić
def dohvatiSveTrenere():
    '''
    Data funkcija vraca sve korisnike iz baze kao json recnik
    :return: vraca listu korisnika
    '''
    sviKorisnici = Korisnik.objects.filter(uloga="trener")
    lista = []
    for elem in sviKorisnici:
        lista.append(elem.__json__())
    return lista


# David Durić
def dohvatiOdgovarajucegTrenera(id):
    '''
    Data funkcija dohvata trenera sa odgovarajucim identifikatorom
    :param id:  Automatski identifikator za svakog trenera
    :return: vraca trenera sa datim identifikatorom
    '''
    trener = Korisnik.objects.get(pk=id)
    return trener


# David Durić
def dohvatiKomentareOTreneru(trener_id):
    '''
    Data funkcija dohvata sve komenentare o treneru sa odgovarajucim identifikatorom
    :param trener_id:  Automatski identifikator za svakog trenera
    :return: vraca komentare o treneru sa odgovarajucim identifikatorom
    '''
    komentari = Komentar.objects.filter(idkomentarisan=trener_id, status=1)
    return komentari


# David Durić
def checkPrivileges(username):
    '''
    :param username: korisnicko ime korisnika
    :return: vraca 0 ako je uloga admin
    vraca 1 ako je uloga trener
    vraca 2 ako je uloga clan
    prosljedjuje joj se korisnicko ime iz requesta: request.user.username
    i vraca se uloga koju ima korisnik
    '''
    try:
        korisnik = Korisnik.objects.get(mejl=username)
    except:
        return -1
    if korisnik.uloga == 'admin':
        return 0
    if korisnik.uloga == 'trener':
        return 1
    if korisnik.uloga == 'clan':
        return 2


# David Durić
def dohvatiPretplate():
    '''
    funkcija sluzi pozadinskoj niti koja ovako dohvata sve poslednje pretplate svih korisnika.
    pretplate su sortirane rastuce po datumu njihovog isteka, sto ce pozadinska nit koristiti da bi znala koliko dugo da spava.
    :return: vraca listu pretplata za datog korisnika
    '''
    pretplate = Pretplata.objects.values('idpretplaceni__mejl').annotate(datumdo=Max('datumdo')).order_by('datumdo')
    listaPretplata = []
    for pretplata in pretplate:
        listaPretplata.append({'korisnik': pretplata['idpretplaceni__mejl'], 'do': pretplata['datumdo']})
    return listaPretplata


# David Durić
def dohvatiPretplateSTerminom():
    '''
    funkcija dohvata iz baze listu korisnika kojima pretplata nije istekla, a broj termina im je dva ili manje.
    :return: vraca listu korisnika
    '''
    danas = datetime.datetime.now(datetime.timezone.utc)
    pretplate = Pretplata.objects.filter(datumdo__gte=danas, preostalotermina=0)
    listaKorisnika = []
    for pretplata in pretplate:
        if Pretplata.objects.filter(datumdo__gte=danas, idpretplaceni=pretplata.idpretplaceni,
                                    idpre__gte=pretplata.idpre, preostalotermina__gt=0):
            continue
        listaKorisnika.append({
            'korisnickiMejl': pretplata.idpretplaceni.mejl,
            'termina': pretplata.preostalotermina
        })
    print(listaKorisnika)
    return listaKorisnika


# David Durić
def ImaAktivnuPretplatu(korisnicko_ime):
    '''
    Provjerava da li korisnik ima aktivnu pretplatu. Korisnik ima aktivnu pretplatu ako ima pretplatu koja vazi danas, i
    pretplatu koja ima jos preostalih termina.
    :param korisnicko_ime: korisnicko ime korisnika
    :return: povratna vrednost je indikator uspesnosti, ukoliko korisnik ima aktivnu pretplatu vraca se True,
    u suprotnom funkcija vraca False
    '''

    # dohvati korisnika za zadatim imenom - ovo ce se uzimati iz logina tako da nije moguce da ne postoji
    k = Korisnik.objects.get(mejl=korisnicko_ime)
    # dohvati najskoriju pretplatu ovog korisnika
    svePretplate = Pretplata.objects.filter(idpretplaceni=k).exclude(preostalotermina=0).order_by('-datumdo')
    if not svePretplate:
        return False
    mojaPretplata = svePretplate[0]
    print(mojaPretplata.datumdo, mojaPretplata.preostalotermina)
    danas = datetime.datetime.now(datetime.timezone.utc)
    if danas <= mojaPretplata.datumdo and mojaPretplata.preostalotermina > 0:
        return True
    return False


# David Durić
def oslobodiTermine(kor_ime, naziv_paketa):
    '''
    Funkcija se zove nakon nove pretplate i sluzi da se oslobode termini koje je mozda stara pretplata pokrivala
    ali nova ne pokriva.
    funkcija prima korisnicko ime i naziv novog paketa na koji je korisnik uspjesno pretplacen
    :param kor_ime: korisnicko ime za datog korisnika
    :param naziv_paketa: naziv paketa
    :return: nema povratne vrednosti
    '''
    # dohvata se korisnik sa odgovarajucim imenom
    korisnik = Korisnik.objects.get(mejl=kor_ime)
    # dohvata se paket sa odgovarajucim nazivom
    paket = Paket.objects.get(naziv=naziv_paketa)
    # dohvataju se tipovi treninga koja obuhvata dati paket, novi paket na koji je korisnik upravo pretplacen.
    obuhvatanja = Obuhvata.objects.filter(idpak=paket.idpak)
    treninzi = set()
    for obuhvatanje in obuhvatanja:
        treninzi.add(obuhvatanje.idtre.tip)
    # dohvata se sve sto korisnik trenutno prati
    pracenja = Prati.objects.filter(idkor=korisnik.idkor)
    # sve sto korisnik prati se brise iz baze ako je onemoguceno dalje pracenje
    for pracenje in pracenja:
        if pracenje.idter.iddrzi.idtre1.tip not in treninzi:
            print(pracenje.idter.iddrzi.idtre1.tip)
            pracenje.delete()


def sviTermini():
    '''
    #Kristina Kragovic
    Ovaj upit dohvata sve informacije o globalnom rasporedu
    :return: povratna vrednost je lista recnika, gdje svaki recnik predstavlja potrebne vrednosti izvucene iz baze -
    dan, vreme pocetka i kraja, salu, tip treninga i koliko je mesta preostalo
    '''
    termini = Termin.objects.all()
    lista = []
    for termin in termini:
        sala = Sala.objects.get(idsala=termin.idpodrzava.idsala_id)
        trening = Trening.objects.get(idtre=termin.idpodrzava.idtre2_id)

        myDict = {
            'Dan': termin.dan,
            'Pocetak': termin.pocetak.strftime('%H:%M'),  # Konvertujemo vreme u string
            'Kraj': termin.kraj.strftime('%H:%M'),  # Konvertujemo vreme u string
            'Sala': sala,
            'Trening': trening,
            'Preostalo': termin.preostalo,
            'IdDrzi': termin.iddrzi,
            'IdTer': termin.idter
        }
        lista.append(myDict)
    return lista


def licniRaspored(korisnik_id, uloga):
    '''
    #Kristina Kragovic
    Ovaj upit dohvata sve informacije o licnom rasporedu, za clana teretane ili trenera u zavisnosti od uloge korisnika
    :param korisnik_id: Automatski generisan identifikator za svakog korisnika
    :param uloga: uloga korisnika
    :return:
    '''
    if uloga == 'clan':
        prati = Prati.objects.filter(idkor=korisnik_id)
        termini = [prat.idter for prat in prati]
    elif uloga == 'trener':
        termini = Termin.objects.filter(iddrzi=korisnik_id)

    lista = []
    for termin in termini:
        sala = Sala.objects.get(idsala=termin.idpodrzava.idsala_id)
        trening = Trening.objects.get(idtre=termin.idpodrzava.idtre2_id)

        myDict = {
            'Dan': termin.dan,
            'Pocetak': termin.pocetak.strftime('%H:%M'),  # Konvertovanje vremena u string
            'Kraj': termin.kraj.strftime('%H:%M'),  # Konvertovanje vremena u string
            'Sala': sala.__json__(),
            'Trening': trening.__json__(),
            'Preostalo': termin.preostalo,
            'IdDrzi': termin.iddrzi,
            'IdTer': termin.idter
        }
        lista.append(myDict)
    return lista


def prijaviTermin(clan_id, termin_id):
    '''
    #Kristina Kragovic
    Ovaj upit dodaje clana cji je id prosledjen da prati termin ciji je id takodje prosledjen
    :param clan_id: Automatski generisan identifikator za svakog clana
    :param termin_id: Automatski generisan identifikator za svaki termin
    :return: ako u terminu nema slobodnih mesta vraca se -1
    ako clan nema uplacenu clanarinu vraca se -2
    inace se clan prijavljuje za termin i smanjuje se broj preostalih mesta tom terminu
    '''

    termin = Termin.objects.get(idter=termin_id)
    clan = Korisnik.objects.get(idkor=clan_id)

    if Prati.objects.filter(idkor=clan_id, idter=termin_id).exists():
        print("Clan vec prati ovaj termin!")
        return -3  # Član već prati termin

    # Provera da li ima slobodnih mesta
    if termin.preostalo <= 0:
        print("Nema slobodnih mesta!")
        return -1  # Nema slobodnih mesta

    pretplate = Pretplata.objects.filter(idpretplaceni=clan_id).exclude(preostalotermina=0).order_by('-datumdo')
    for pretplata in pretplate:
        print(pretplata.datumdo, pretplata.idpre)
    pretplata = pretplate[0]
    print("MOJA AKTIVNA PRETPLATA")
    print(pretplata.datumdo, pretplata.idpre)
    pokriva = Pokriva.objects.filter(idpre=pretplata.idpre, idtre=termin.iddrzi.idtre1)
    if not pokriva:
        print("Vasa pretplata trenutno ne pokriva tip treninga " + termin.iddrzi.idtre1.tip)
        return -2
    termin.preostalo -= 1
    termin.save()

    prati = Prati(idkor=clan, idter=termin)
    prati.save()

    return 0


def dodajTermin(trener_id, tip_treninga, sala_id, dan, pocetak, kraj, brojMesta):
    '''
    #Kristina Kragovic
    ovaj upit dodaje treneru ciji je id prosledjen, termin sa informacijama koje su prosledjene
    mozda treba da se proveri i da l je trener zauzet u tom terminu
    inace se dodaje termin
    :param trener_id: Automatski generisan identifikator za svakog trenera
    :param tip_treninga: tip treninga
    :param sala_id: Automatski generisan identifikator za svaku salu
    :param dan: dan kada se dodaje termin
    :param pocetak: pocetak termina
    :param kraj: kraj termina
    :param brojMesta: broj mesta u terminu
    :return: ukoliko je termin zauzet vraca se -1, a u slucaju uspeha dodaje se termin i vraca se 0
    '''

    trener = Korisnik.objects.get(idkor=trener_id, uloga='trener')
    trening = Trening.objects.get(tip=tip_treninga)
    sala = Sala.objects.get(idsala=sala_id)

    # Provera da li je termin zauzet
    if Termin.objects.filter(dan=dan, kraj=kraj, pocetak=pocetak, idpodrzava=sala_id).exists():
        return -1  # Termin je zauzet

    try:
        drzi = Drzi.objects.get(idkor=trener_id, idtre1=trening.idtre)  # mozda ide samo trening

    except Drzi.DoesNotExist:
        print("Trener ne drzi dati trening")
        return -2

    podrzava = Podrzava.objects.get(idsala=sala_id, idtre2=trening.idtre)

    # Kreiranje novog termina
    novi_termin = Termin.objects.create(
        dan=dan,
        pocetak=pocetak,
        kraj=kraj,
        idpodrzava=podrzava,
        iddrzi=drzi,
        preostalo=brojMesta
    )
    novi_termin.save()
    return 0  # Uspešno dodat termin


def drzi_treninge(id_kor):
    '''
    #David Duric 2021/0102
    funkcija eliminise treninge koje korisnik ne drzi
    :param id_kor:  Automatski generisan identifikator za svakog korisnika
    :return: povratna vrednost je lista treninga
    '''
    drzi = Drzi.objects.filter(idkor=id_kor)
    treninzi = []
    for d in drzi:
        treninzi.append({'Tip': d.idtre1.tip, 'idtre': d.idtre1.idtre})
    print(treninzi)
    return treninzi


def odjaviTermin(clan_id, termin_id):
    '''
    # Kristina Kragovic
    ovaj upit radi ukanjanje termina ciji je d prosledjen,  clanu teretane ciji je id takodje prosledjen
    :param clan_id: Automatski generisan identifikator za svakog clana
    :param termin_id: Automatski generisan identifikator za svaki termin
    :return: povratna vrednost je 0
    '''

    Prati.objects.filter(idkor=clan_id, idter=termin_id).delete()
    termin = Termin.objects.get(idter=termin_id)
    termin.preostalo += 1
    termin.save()

    return 0


def ukloniTermin(trener_id, termin_id):
    '''
    # Kristina Kragovic
    ovaj upit uklanja termin ciji je id prosledjen, treneru ciji je id takodje prosledjen
    nakon uklanjanja termina, clanovi teretane koji su bili prijavljeni bice o tome obavesteni putem mejla
    :param trener_id: Automatski generisan identifikator za svakog trenera
    :param termin_id: Automatski generisan identifikator za svaki termin
    :return: povratna vrednost je 0
    '''

    termin = Termin.objects.get(idter=termin_id)
    trener = Korisnik.objects.get(idkor=trener_id)

    # Dobijanje prijavljenih članova na terminu
    prijavljeni_clanovi = Prati.objects.filter(idter=termin_id)

    # Slanje automatskog mejla obaveštenja prijavljenim članovima
    for clan in prijavljeni_clanovi:
        subject = 'Obaveštenje o otkazivanju termina'
        message = f'Poštovani {clan.idkor.mejl},\n\nObaveštavamo vas da je termin "{termin.iddrzi.idtre1.tip}" u kojem ste bili prijavljeni kod trenera {trener.mejl} otkazan.\n\nHvala vam na razumevanju.\n\nS poštovanjem,\nStepByStep centar'
        recipient_list = [clan.idkor.mejl]
        send_new_email(recipient_list, subject, message)

    termin.delete()
    return 0


def autorizacija_administratora(korisnicko_ime, lozinka):
    '''
    # Kristina Kragovic
    ovaj upit radi autorizaciju administratora sa zadatim korisnickim imenom i lozinkom
    :param korisnicko_ime: Automatski generisan identifikator za svaki termin
    :param lozinka: Automatski generisan identifikator za svaki termin
    :return: funkcija vraca -1 ukoliko korisnik sa datim korisnickim imenom ne postoji
    funkcija vraca -2 ukoliko je neispravna lozinka
    funkcija vraca -3 ukolko korisnik nema ulogu administratora
    inace je provera uspesna
    '''
    try:
        korisnik = Korisnik.objects.get(mejl=korisnicko_ime)
    except Korisnik.DoesNotExist:
        return -1

    # Provera ispravnosti lozinke
    if not check_password(lozinka, korisnik.sifra):
        return -2

    # Provera da li je korisnik administrator
    if korisnik.uloga == 'admin':
        # Korisnik je administrator
        return 0
    else:
        # Korisnik nije administrator
        return -3


def autorizacija_trenera(korisnicko_ime, lozinka):
    '''
    # Kristina Kragovic
    ovaj upit radi autorizaciju administratora sa zadatim korisnickim imenom i lozinkom
    :param korisnicko_ime: korisnicko ime trenera
    :param lozinka: lozinka trenera
    :return: funkcija vraca -1 ukoliko korisnik sa datim korisnickim imenom ne postoji
    funkcija vraca -2 ukoliko je neispravna lozinka
    funkcija vraca -3 ukolko korisnik nema ulogu administratora
    inace je provera uspesna
    '''
    try:
        korisnik = Korisnik.objects.get(mejl=korisnicko_ime)
    except Korisnik.DoesNotExist:
        return -1

    # Provera ispravnosti lozinke
    if not check_password(lozinka, korisnik.sifra):
        return -2

    # Provera da li je korisnik administrator
    if korisnik.uloga == 'trener':
        # Korisnik je administrator
        return 0
    else:
        # Korisnik nije administrator
        return -3


def autorizacija_clana_teretane(korisnicko_ime, lozinka):
    '''
    # Kristina Kragovic
    ovaj upit radi autorizaciju administratora sa zadatim korisnickim imenom i lozinkom
    :param korisnicko_ime: korisnicko ime clana teretane
    :param lozinka: lozinka clana teretane
    :return: funkcija vraca -1 ukoliko korisnik sa datim korisnickim imenom ne postoji
    funkcija vraca -2 ukoliko je neispravna lozinka
    funkcija vraca -3 ukolko korisnik nema ulogu clana teretane
    inace je provera uspesna
    '''
    try:
        korisnik = Korisnik.objects.get(mejl=korisnicko_ime)
    except Korisnik.DoesNotExist:
        return -1

    # Provera ispravnosti lozinke
    if not lozinka == korisnik.sifra:
        return -2

    # Provera da li je korisnik administrator
    if korisnik.uloga == 'clan':
        # Korisnik je administrator
        return 0
    else:
        # Korisnik nije administrator
        return -3


def registracija_korisnika(mejl, sifra):
    '''
    # Kristina Kagovic
    ovaj upit ce raditi registraciju korisnika
    ako funkcija vrati -1 to znaci da mejl vec postoji u bazi
    inace se radi potvrda registracije preko mejla i ako nema problema
    dodaje se novi korisnik u sistem
    :param mejl: mejl korisnika
    :param sifra: sifra korisnika
    :return: povratna vrednost je 0
    '''

    # Provera da li korisnik već postoji u bazi
    if Korisnik.objects.filter(mejl=mejl).exists():
        return -1
    # Kreiranje novog korisnika
    korisnik = Korisnik(
        mejl=mejl,
        uloga='clan',  # Postavljanje uloge na 'clan' za registrovane korisnike
        sifra=sifra,  # Čuvanje šifre korisnika u hashiranom obliku
    )
    korisnik.save()
    user = User.objects.create_user(username=mejl, password=sifra)
    user.save()
    return 0


def korisnikPostoji(korisnickoIme):
    '''
    #David Duric
    Ova funkcija samo provjerava da li korisnik postoji
    :param korisnickoIme: korisnicko ime korisnika
    :return: povratna vrednost je True ukoliko korisnik postoji, u suprotnom se vraca False
    '''
    if Korisnik.objects.filter(mejl=korisnickoIme).exists():
        return True
    return False


def dodaj_trenera(korisnicko_ime, sifra, tipovi_treninga, image_data):
    '''
    # Kristina Kragovic
    Ovaj upit ce raditi dodavanje novog trenera, sa tipovima treninga koje moze da drzi
    Ako funkcija vrati -1 to znaci da je korisnicko ime zauzeto
    Inace je uspesno dodat trener u bazu.
    :param korisnicko_ime: korisnicko ime korisnika
    :param sifra: sifra korisnika
    :param tipovi_treninga: tipovi treninga za trenera
    :param image_data: slika trenera
    :return: u slucaju uspeha se vraca 0, a u slucaju da postoji korisnicko ime se vraca -1
    '''

    # Provera da li je korisničko ime jedinstveno
    if Korisnik.objects.filter(mejl=korisnicko_ime).exists() or User.objects.filter(
            username=korisnicko_ime).exists():
        return -1

    # Kreiranje korisnika sa ulogom 'trener'
    trener = Korisnik.objects.create(
        mejl=korisnicko_ime,
        uloga='trener',
        sifra=sifra,
        slika=image_data.read()
    )

    # Dodavanje tipova treninga koje trener može da drži
    for tip_treninga_id in tipovi_treninga:
        trening = Trening.objects.get(idtre=tip_treninga_id)
        Drzi.objects.create(idkor=trener, idtre1=trening)

    return 0


def ukloni_trenera(trener_id):
    # Kristina Kragovic
    # ovaj upit ce raditi uklanjanje trenere iz baze koje administrator selektovao
    # funkcija vraca -1 ukoliko ni jedan trener nije izabran
    # inace vraca 0, a svi clanovi koji su pratili termine obrisanih trenera bice o tome obavesteni
    # Provera da li postoji korisnik (trener) sa datim ID-om i ulogom 'trener'
    try:
        trener = Korisnik.objects.get(idkor=trener_id, uloga='trener')
        trener_auth = User.objects.get(username=trener.mejl)
    except Korisnik.DoesNotExist:
        print(f"Trener sa ID-em {trener_id} ne postoji.")
        return
    except Korisnik.MultipleObjectsReturned:
        print(f"Pronadjeno je vise trenera sa ID-em {trener_id}.")
        return

    termini_trenera_ids = list(Termin.objects.filter(iddrzi__idkor=trener_id).values_list('idter', flat=True))

    print("Termini trenera IDs:", termini_trenera_ids)

    korisnici_pratili_ids = list(Prati.objects.filter(idter__in=termini_trenera_ids).values_list('idkor', flat=True))

    for korisnik_id in korisnici_pratili_ids:
        try:
            korisnik = Korisnik.objects.get(idkor=korisnik_id)
            print("Korisnik koji se obavestava:", korisnik.mejl)
            subject = 'Obaveštenje o uklanjanju trenera'
            message = f'Poštovani {korisnik.mejl},\n\nObaveštavamo vas da je trener {trener.mejl} uklonjen iz sistema. Molimo vas da proverite svoj raspored i izaberete druge termine.\n\nHvala vam na razumevanju.\n\nS poštovanjem,\nStep by Step'
            recipient_list = [korisnik.mejl]
            send_new_email(recipient_list, subject, message)
        except Korisnik.DoesNotExist:
            print(f"Korisnik sa ID-em {korisnik_id} ne postoji.")
            continue

    Termin.objects.filter(iddrzi__idkor=trener_id).delete()

    trener.delete()
    trener_auth.delete()
    return 0


def dohvatanje_id_treninga(tip_treninga):
    '''
    #Kristina Kragovic
    ova funkcija dohvata treninge po nazivu
    :param tip_treninga: tip treninga
    :return: vraca zadati trening
    '''
    trening = Trening.objects.get(tip=tip_treninga)
    return trening.idtre


def uredi_trenera(trener_id, novi_tipovi_treninga, image_data):
    '''
    #Kristina Kragovic
    ovaj upit ce treneru sa datim Id-em dodati prosledjeni tipovi treninga
    inace je trener uspesno uredjen
    :param trener_id: Automatski generisan identifikator za svakog trenera
    :param novi_tipovi_treninga: novi tipovi treninga za trenera pri izmeni
    :param image_data: slika trenera
    :return: povratna vrednost je 0
    '''

    # Dobijanje objekta trenera
    trener = Korisnik.objects.get(idkor=trener_id, uloga='trener')
    if image_data is not None:
        trener.slika = image_data.read()
        trener.save()
    # Provera da li trener vec drzi sve treninge koji su mu dodati
    trening_drzi = Drzi.objects.filter(idkor=trener_id).values_list('idtre1', flat=True)

    treninzi_za_dodavanje = []
    for i in range(0, len(novi_tipovi_treninga)):
        if novi_tipovi_treninga[i] in trening_drzi:
            continue
        else:
            treninzi_za_dodavanje.append(novi_tipovi_treninga[i])

    #   if set(novi_tipovi_treninga).issubset(trening_drzi):
    #   return -1, "Trener vec drzi sve odabrane treninge."

    # Dodavanje novih treninga treneru
    for tip_treninga_id in treninzi_za_dodavanje:
        # Dodavanje drzanja treninga treneru
        trening = Trening.objects.get(idtre=tip_treninga_id)
        drzi = Drzi(idkor=trener, idtre1=trening)
        drzi.save()

    return 0


def dohvatiKomentareOTeretani():
    '''
    #Krisitna Kragovic
    Data funkcija dohvata komentare o teretani, a zatim vrsi njihovo filtriranje na osnovu statusa i idkomentarisan
    :return: vraca izlistane komentare o teretani
    '''
    komentari = Komentar.objects.filter(idkomentarisan=None, status=1)
    return komentari


def kreiraj_komentar(tekst, trener_id, idautor):
    '''
    Data funkcija kreira komentar za datog trenera
    :param tekst: tekstualni opis komentara
    :param trener_id: Automatski generisan identifikator za svakog trenera
    :param idautor: Automatski generisan identifikator za svakog autora
    :return: vraca dati komenatr
    '''

    autor = Korisnik.objects.get(idkor=idautor)
    datum = datetime.datetime.now(datetime.timezone.utc)
    if trener_id:
        komentarisan = Korisnik.objects.get(idkor=trener_id)
    else:
        komentarisan = None

    komentar = Komentar(
        tekst=tekst,
        status=0,
        datum=datum,
        idautor=autor,
        idkomentarisan=komentarisan
    )
    komentar.save()
    return komentar


def sviTreneri(request):
    '''
    #Krisitna Kragovic
    Data funkcija dohvata sve trenere
    :param request: Zahtev prosledjen serveru
    :return: vraca korisnike sa ulogom trener
    '''
    return Korisnik.objects.all(uloga="trener")


def sviTreninziKojeTrenerNeDrzi(trener_id):
    '''
    #Kristina Kragovic
    Ova metoda vraća sve tipove treninga koje trener ne drži
    :param trener_id: ID trenera čije treninge želimo isključiti
    :return: Vraća listu rečnika, a svaki rečnik ima definisano polje Tip
    '''
    trener_drzi = Drzi.objects.filter(idkor_id=trener_id).values_list('idtre1_id', flat=True)
    treninzi = Trening.objects.exclude(idtre__in=trener_drzi)

    lista = []
    for trening in treninzi:
        lista.append(trening.__json__())
    return lista


def dohvatiKomentare():
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija dohvata sve komentare o teretani
    :return: povratnu vrednost predstavljaju izlistani komentari sa svojim atributima koji su izvuceni iz baze podataka-
    idkom, tekst, status, datum, ida, idkomentarisan
    '''
    komentari = Komentar.objects.all()
    print(komentari)
    return komentari


def dohvatiNeodobreneKomentare():
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija dohvata sve neodobrene komentare o treneru, tako sto filtrira sve komentare, cija je vrednost statusa jednaka nuli
    :return: povratnu vrednost predstavljaju izlistani neodobreni komentari sa svojim atributima koji su izvuceni iz baze podataka -
    idkom, tekst, status, datum, ida, idkomentarisan
    '''
    komentari = Komentar.objects.filter(status=0)
    return komentari


def odobriKomentar(id_kom):
    # Sofija Martinovic 0486/2021
    '''
    data funkcija vrsi obobravanje komentare za trenera, tako sto dohvata id komentara koji treba da se odobri
    zatim kada dohvati komentar, vrsi promenu u bazi tako sto u tabeli Komentar u polje status upisuje 1 za taj komentar
    na kraju se cuva izmena u bazi
    :param id_kom: Automatski generisan identifikator za svaki komentar
    :return: nema, promene se cuvaju u bazi
    '''
    komentar = Komentar.objects.get(idkom=id_kom)
    komentar.status = 1
    komentar.save()


def obrisiKomentar(id_kom):
    # Sofija Martinovic 0486/2021
    '''
    data funkcija brise komentare iz baze koji nisu odobreni
    prvo se filtriraju dati komentari i oni komentari koji imaju status 0 se brisu iz baze uz pomoc funkcije delete
    :param id_kom: Automatski generisan identifikator za svaki komentar
    :return: nema, promene se cuvaju u bazi
    '''
    Komentar.objects.filter(idkom=id_kom).delete()


def dohvatiOdgovarajuciPaket(paket_id):
    # Sofija Martinovic 0486/2021
    '''
    data funkcija dohvata odgovarajuci paket sa zadatim id
    :param paket_id: Automatski generisan identifikator za svaki paket
    :return: povratnu vrednost predstavlja dati paket
    '''
    paket = Paket.objects.get(idpak=paket_id)
    return paket


def dohvati_sale():
    # Sofija Martinovic 0486/2021
    '''
    data funkcija dohvata sve sale iz baze podataka
    :return: povratnu vrednost predstavljaju izlistane sale sa svojim atributima koji su izvuceni iz baze podataka -
    idsala,naziv
    '''
    sala = Sala.objects.all()
    print(sala)
    return sala


def dohvati_treninge_za_paket(paketi):
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija dohvata sve treninge za dati paket
    :param paketi: paket
    :return: nema
    '''
    paketi_data = []
    print("PAKETI")

    for paket in paketi:
        print(paket)


def sviPrati():
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija dohvata sve podatke iz tabele Prati
    :return: povratnu vrednost predstavljaju izlistani atributi iz tabele Prati koji su izvuceni iz baze podataka -
    idprati,idkor,idter
    '''
    return Prati.objects.all()


def pratiOdredjenTermin(id_ter):
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija dohvata samo odredjeni termin koji se prati
    :param id_ter: Automatski generisan identifikator za svaki termin
    :return: vraca flitriranu listu atributa po idterminu iz tabele Prati
    '''
    return Prati.objects.filter(idter=id_ter)


def pretplateOdredjenogKorisnika(id_kor):
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija izlistava podatke iz tabele Pretplata za datog korisnika i sortira ih po datumu i kao
    rezultat dobijamo listu pretplata za datog korisnika
    :param id_kor: Automatski generisan identifikator za svakog korisnika
    :return: vraca filtriranu listu pretplata za datog korisnika
    '''

    return Pretplata.objects.filter(idpretplaceni=id_kor).exclude(preostalotermina=0).order_by('-datumdo').first()


def pratiObrisiKorisnika(id_kor, termin):
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija vrsi brisanje datog korisnika iz termina koji prati
    :param id_kor: Automatski generisan identifikator za svakog korisnika
    :param termin: termin
    :return: nema
    '''
    prati = Prati.objects.filter(idkor=id_kor, idter=termin)
    for p in prati:
        p.delete()


def dohvatiKorisnikaPoId(id_kor):
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija dohvata korisnika sa zadatim id_kor
    :param id_kor: Automatski generisan identifikator za svakog korisnika
    :return: vraca datog korisnika
    '''
    return Korisnik.objects.get(idkor=id_kor)


def dohvatiTerminPoId(id_ter):
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija dohvata termin sa zadatim id_ter
    :param id_ter: Automatski generisan identifikator za svaki termin
    :return: vraca dati termin
    '''
    return Termin.objects.get(idter=id_ter)


def dohvatiPaketPoId(id_pak):
    # Sofija Martinovic 0486/2021
    '''
    Data funkcija dohvata paket sa zadatim id_pak
    :param id_pak: Automatski generisan identifikator za svaki paket
    :return: vraca dati paket
    '''
    return Paket.objects.get(idpak=id_pak)


def pokrivaPretplata(id_pre):
    return Pokriva.objects.filter(idpre=id_pre)
