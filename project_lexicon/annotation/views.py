from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.forms import inlineformset_factory
from django.forms.models import model_to_dict

from lexicon.models import Source
from .models import AnnotationScheme, AnnotationLabel, Annotation

from lexicon.notes import SourceListView, NavigateSource


class AnnotationSourceListView(SourceListView):
    template_name = 'annotation/annotation_list_source.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        scheme = AnnotationScheme.objects.get(pk=self.kwargs['scheme_id'])
        ctx['scheme'] = scheme
        return ctx


class AnnotationNavigateSource(NavigateSource):
    template_name = 'annotation/annotation_navigate_source.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        scheme = AnnotationScheme.objects.get(pk=self.kwargs['scheme_id'])
        ctx['scheme'] = scheme
        ctx['url'] = reverse('annotate_nav_source', args=[scheme.pk]) + '?' + ctx['query_dict'].urlencode()
        ctx['base_page'] = reverse('annotate_list_source', args=[scheme.pk]) + '?' + ctx['query_dict'].urlencode()        
        return ctx


class AnnotationSchemeIndex(generic.ListView):
    template_name = 'annotation/list_schemes.html'
    context_object_name = 'schemes'
    model = AnnotationScheme 


class CreateAnnotationScheme(generic.edit.CreateView):
    template_name = 'annotation/create_scheme.html'
    model = AnnotationScheme
    fields = ['name', 'aim']
    success_url = reverse_lazy('list_schemes')


class ViewAnnotationScheme(generic.DetailView):
    model = AnnotationScheme
    template_name = 'annotation/view_scheme.html'


def add_labels_to_scheme(request, scheme_id):
    scheme = AnnotationScheme.objects.get(pk=scheme_id)
    LabelFormSet = inlineformset_factory(AnnotationScheme, AnnotationLabel, fields='name definition examples extra_rules'.split())
    formset = LabelFormSet(instance=scheme)
    if request.method == 'POST':
        formset = LabelFormSet(request.POST, instance=scheme)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('view_scheme', args=[scheme.id]))
    ctx = {'formset':formset, 'object':scheme}
    return render(request, 'annotation/add_labels_to_scheme.html', ctx)
    

class CreateAnnotationLabel(generic.edit.CreateView):
    template_name = 'annotation/label_create.html'
    model = AnnotationLabel
    fields = ['name', 'definition', 'examples', 'extra_rules']


class AnnotationLabelIndex(generic.ListView):
    template_name = 'annotation/label_index.html'
    context_object_name = 'labels'
    model = AnnotationLabel


def create_annotation(request):
    try:
        label_id = int(request.GET.get('label', None))
        label = AnnotationLabel.objects.get(pk=label_id)
        occurrence_id = int(request.GET.get('occurrence', None))
        occurrence = Source.objects.get(pk=occurrence_id)
        
        annotation = Annotation.objects.create(
            label=label,
            scheme=label.scheme
            )
        annotation.source_tokens.add(occurrence)

        return JsonResponse({'response':True})  
    except:
        return JsonResponse({'response':False})  