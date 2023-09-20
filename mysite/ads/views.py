from typing import Any
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import generic 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ad, Comment, Fav
from .forms import AdCreateForm, CommentForm


class AdListView(generic.ListView):
    model = Ad 
    template_name = 'ads/ad_list.html'
    context_object_name = 'ad_list' 
    search_fields = ['title', 'tags']
    paginate_by = 20
    
    def get_queryset(self) -> QuerySet[Any]:
        query_set =  super().get_queryset()
        search = self.request.GET.get('search')
        tag_name = self.kwargs.get('tag_name', None)
        if search:  
            query_set = Ad.objects.filter(Q(title__icontains=search) | Q(tags__name__icontains=search))
            
        elif tag_name : 
            query_set = Ad.objects.filter(tags__name__iexact=tag_name)
         
        return query_set.order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # If the user is authenticated, fetch their favorite ads
        if self.request.user.is_authenticated:
            favorite_ads = Fav.objects.filter(user=self.request.user).values_list('ad_id', flat=True)
            context['favorites'] = list(favorite_ads)
        else:
            context['favorites'] = []

        return context
    
    
    
    
class AdCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ad
    form_class = AdCreateForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object =  form.save()  # self.object is convention in Django.
        form.save_m2m()
        return super().form_valid(form)

class AdUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ad 
    form_class = AdCreateForm 
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')
    def form_valid(self, form: BaseModelForm) :
        form.instance.owner = self.request.user
        return super().form_valid(form)
        
class AdDetailView(generic.DeleteView):
    model = Ad
    template_name = "ads/ad_detail.html"
    def get(self, request, pk) :
        x = get_object_or_404(Ad, id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }

        return render(request, self.template_name, context)
        
        
class AdDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ad 
    context_object_name = 'ad'           # no need to add template_name if I followed the convention.
    success_url = reverse_lazy('ads:ad_list')
def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    if ad.content_type:
        response = HttpResponse()
        response['Content-Type'] = ad.content_type
        response['Content-Length'] = len(ad.picture)
        response.write(ad.picture)
        return response
        
    
class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        form = CommentForm(request.POST)                                # we can use form_valid and  get_succsess_url instead 
        current_ad = Ad.objects.get(id=self.kwargs['pk'])
        if form.is_valid():
            to_save_model_instance= form.save(commit=False)
            to_save_model_instance.owner = self.request.user 
            to_save_model_instance.ad = current_ad 
            
            to_save_model_instance.save()
        else :
            form = CommentForm()  
            
        return redirect(reverse('ads:ad_detail', kwargs={'pk': self.kwargs['pk']}))
    
    
class CommentDeleteView(LoginRequiredMixin, generic.DeleteView): 
    model = Comment
    template_name = "ads/comment_confirm_delete.html"
    def get_queryset(self):
        query = Comment.objects.filter(owner = self.request.user)
        return query
    def get_success_url(self):
        ad = self.object.ad   # the object I deleted
        return reverse('ads:ad_detail', args=[ad.id])
    
    
    
def fav_add(request, pk):
    if request.method== 'POST' and request.user.is_authenticated:
        ad = get_object_or_404(Ad, id=pk)
        if not Fav.objects.filter(ad=ad, user=request.user).exists():
            
            fav = Fav(ad=ad, user=request.user) 
            fav.save()
            return JsonResponse({'message':'success'}, status=200)
        else : 
            return JsonResponse({'error': 'Already favorited'}, status=400)
             
    else: 
        return JsonResponse({'error': 'not post or user not authen'}, status=400)
    
  
def fav_remove(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        ad = get_object_or_404(Ad, id=pk)
        
        # Check if the fav record exists
        fav_record = Fav.objects.filter(ad=ad, user=request.user).first()
        
        if fav_record:
            fav_record.delete()
            return JsonResponse({'message':'success'}, status=200)
    else: 
        return JsonResponse({'error': 'not post or user not authen'}, status=400)
    
    
    
    
from taggit.models import Tag

def tag_view(request, tag_name):
    # You can use the `tagged_with` method provided by django-taggit
    query_set = Ad.objects.filter(tags__name__iexact=tag_name)
    context = {'ad_list': query_set}
    if request.user.is_authenticated:
        favorite_ads = Fav.objects.filter(user=request.user).values_list('ad_id', flat=True)
        context['favorites'] = list(favorite_ads)
    return render(request, 'ads/ad_list.html', context=context)
