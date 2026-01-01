from django.http import JsonResponse
from core.models import Author


def read_all(request):
    authors = Author.objects.all()
    authors_list = [author.to_dict() for author in authors]
    return JsonResponse(
        authors_list,
        safe=False,
    )


def read_one(request, author_id):
    author = Author.objects.get(id=author_id)
    return JsonResponse(
        author.to_dict(),
        safe=False,
    )
