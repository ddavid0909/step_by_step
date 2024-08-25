from django.http import HttpResponse

from proj.models import Korisnik


def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if args:
                request = args[0]
                print(request.user.username)
                korisnik = Korisnik.objects.get(mejl=request.user.username)
                if (korisnik.uloga == role):
                    return func(*args, **kwargs)
                return HttpResponse("Better luck next time :)")
        return wrapper
    return decorator