from queue import Queue

from django.core.mail import send_mail
#David Duric
#Funkcija prima kod i primaoca, formatira poruku i salje je.
queue = Queue()
def code_mail(to, code):
    subject = 'Potvrdni kod za registraciju'
    message = f'Vaš kod je {code}'
    send_new_email([to], subject, message)


#David Duric
#Funkcija prima sadrzaj mejla i LISTU primalaca
def send_new_email(to, subject, message):
   # send_mail(subject, message, 'stepbysteppsi@outlook.com', to)
    queue.put((subject, message,'stepbysteppsi@outlook.com', to))


