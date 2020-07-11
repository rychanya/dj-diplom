from app.models import Menu


def menu_context(request):
    return {"meny_iteams": Menu.objects.all()}
