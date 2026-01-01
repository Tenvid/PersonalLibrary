from django.http import JsonResponse
from core.models import Publisher


def read_all(request):
    publishers = Publisher.objects.all()
    publishers_list = [publisher.to_dict() for publisher in publishers]
    return JsonResponse(
        publishers_list,
        safe=False,
    )
