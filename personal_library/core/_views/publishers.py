from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from core.models import Publisher
from django.views.generic.list import ListView


class PublishersListView(ListView):
    model = Publisher
    template_name = "core/publishers.html"
    context_object_name = "publishers"
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return Publisher.objects.filter(name__icontains=query)
        return Publisher.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = "core/publisher_detail.html"
    context_object_name = "publisher"

    def get_object(self) -> Publisher:
        slug = self.kwargs.get("slug")
        return get_object_or_404(Publisher, slug=slug)


class PublisherEditView(UpdateView):
    model = Publisher
    template_name = "core/publisher_edit.html"
    fields = ["name", "country", "slug"]

    def get_success_url(self):
        return reverse("publisher_detail", kwargs={"slug": self.object.slug})


class PublisherCreateView(CreateView):
    model = Publisher
    template_name = "core/publisher_edit.html"
    fields = ["name", "country", "slug"]

    def get_success_url(self):
        return reverse("publisher_detail", kwargs={"slug": self.object.slug})
