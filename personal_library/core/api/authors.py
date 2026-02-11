from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from core.models import Author


def read_all(request):
    authors = Author.objects.all()
    authors_list = [author.to_dict() for author in authors]
    return JsonResponse(
        authors_list,
        safe=False,
    )


def read_one(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
        return JsonResponse(
            author.to_dict(),
            safe=False,
        )
    except Author.DoesNotExist:
        return HttpResponse(status=404)


def create(request):
    name = request.POST.get("name")
    biography = request.POST.get("biography")

    author = Author.objects.create(name=name, biography=biography)
    return redirect("/authors/")


def update(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return HttpResponse(status=404)

    name = request.POST.get("name")
    biography = request.POST.get("biography")

    author.name = name
    author.biography = biography
    author.save()

    return redirect("/authors/")


def delete(request, author_slug):
    try:
        author = Author.objects.get(slug=author_slug)
        author.delete()
        return redirect("/authors/")
    except Author.DoesNotExist:
        return HttpResponse(status=404)
