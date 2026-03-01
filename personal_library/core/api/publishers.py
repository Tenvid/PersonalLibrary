from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from core.models import Publisher


def read_all(request):
    publishers = Publisher.objects.all()
    publishers_list = [publisher.to_dict() for publisher in publishers]
    return JsonResponse(
        publishers_list,
        safe=False,
    )


def read_one(request, publisher_id):
    try:
        publisher = Publisher.objects.get(id=publisher_id)
        return JsonResponse(
            publisher.to_dict(),
            safe=False,
        )
    except Publisher.DoesNotExist:
        return HttpResponse(status=404)


def create(request):
    name = request.POST.get("name")
    country = request.POST.get("country")

    publisher = Publisher.objects.create(name=name, country=country)  # noqa
    return redirect("/publishers/")


def update(request, publisher_id):
    try:
        publisher = Publisher.objects.get(id=publisher_id)
    except Publisher.DoesNotExist:
        return HttpResponse(status=404)

    name = request.POST.get("name")
    country = request.POST.get("country")

    publisher.name = name
    publisher.country = country
    publisher.save()

    return redirect("/publishers/")


def delete(request, publisher_slug):
    try:
        publisher = Publisher.objects.get(slug=publisher_slug)
        publisher.delete()
        return redirect("/publishers/")
    except Publisher.DoesNotExist:
        return HttpResponse(status=404)
