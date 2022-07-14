from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, Photo
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .forms import ItemForm, CommentForm
import uuid
import boto3
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'marketshop-7'

def home (request):
    return render(request, 'home.html')

def item_index(request):
    items = Item.objects.all()
    return render(request, 'items/index.html', {'items':items})

@login_required
def listing(request):
    items = Item.objects.filter(user = request.user)
    return render(request, 'items/listing.html', {'items': items})

def items_detail(request, item_id):
    comment_form = CommentForm()
    item = Item.objects.get(id=item_id)
    return render(request, 'items/detail.html', {
        'item':item,'comment_form':comment_form })

def signup(request):
    error_message = ''
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid Sign Up, please try again'
    form = UserCreationForm()
    context = {'form':form, 'error_message':error_message}
    return render(request, 'registration/signup.html', context)

class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields  = ['name','category','price','description']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    # model = Item
    # fields ='__all__'
    # success_url = '/items/browse'
    # def get_absolute_url(self):
    #     return reverse('detail', kwargs={'item_id':self.id})

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'category', 'price', 'description']

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/items/browse/'

@login_required
def add_photo(request, item_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to item_id or cat (if you have a cat object)
            photo = Photo(url=url, item_id=item_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('item_detail', item_id=item_id)


# class CommentCreate(LoginRequiredMixin, CreateView):
#     model = Item
#     fields  = ['text']
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)   

@login_required
def add_comment(request, item_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.item_id = item_id
        new_comment.user = request.user
        new_comment.save()
    return redirect('item_detail', item_id = item_id)