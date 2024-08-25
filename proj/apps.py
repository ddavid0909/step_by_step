import datetime
import time

from django.apps import AppConfig
import os
from threading import Thread

from django.core.mail import send_mail


class MailThread(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    def run(self) -> None:
        while True:
            address_info = self.queue.get()
            send_mail(*address_info)

"""
class IstekTermina(Thread):
    def __init__(self, func, mails):
        super().__init__()
        self.func = func
        self.mails = mails

    def run(self) -> None:
        while True:
            listaPretplata = self.func()
            print(listaPretplata)
            for pretplata in listaPretplata:
                self.mails([pretplata['korisnickiMejl']], 'Potroseni termini', "Obaveštavamo Vas da ste potrošili sve termine. Vaš Step By Step")
            time.sleep(86400)
"""

class IstekPretplate(Thread):
    def __init__(self, func, mails):
        super().__init__()
        self.func = func
        self.mails = mails
    def run(self) -> None:

        while True:
            listaPretplata = self.func()
            print(listaPretplata)
            if not listaPretplata:
                time.sleep(86400)
                continue
            danas = datetime.datetime.now(datetime.timezone.utc)
            print(danas)
            for pretplata in listaPretplata:
                if (datetime.timedelta(0) <= pretplata['do'] - danas <= datetime.timedelta(3)):
                    self.mails([pretplata['korisnik']], 'Vaša pretplata ubrzo ističe!', 'Obaveštavamo Vas da Vaša pretplata ističe za manje od četiri dana! Vaš Step By Step.')

                elif (danas - pretplata['do'] == datetime.timedelta(days=-1)):
                    print(danas-pretplata['do'])
                    self.mails([pretplata['korisnik']], 'Istekla pretplata',
                               'Obaveštavamo Vas da je Vaša pretplata istekla. Ovo Vas ne izbacuje automatski sa treninga koje pratite,'
                               'ali je potrebno da što pre obnovite pretplatu. Vaš Step By Step')

            print("Sleep a day out")
            time.sleep(86400)


class ProjConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proj"

    def ready(self):
        from proj.models import dohvatiPretplateSTerminom
        from proj.models import dohvatiPretplate
        from proj.mail import send_new_email, queue

        if os.environ.get('RUN_MAIN'):
           IstekPretplate(dohvatiPretplate, send_new_email).start()
          # IstekTermina(dohvatiPretplateSTerminom, send_new_email).start()
           MailThread(queue).start()


