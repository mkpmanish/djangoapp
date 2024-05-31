from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world! --- Manish")




def find_user(username):
    with connection.cursor() as cur:
        cur.execute(f"""select username from USERS where name = '%s'""" % username)
        output = cur.fetchone()
    return output
