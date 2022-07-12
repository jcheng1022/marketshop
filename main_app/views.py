from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .forms import ItemForm
# Create your views here.


def home (request):
    return render(request, 'home.html')

def item_index(request):
    items = Item.objects.all()
    return render(request, 'items/index.html', {'items':items})

def items_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'items/detail.html', {
        'item':item})

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

class ItemCreate(CreateView):
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

class ItemUpdate(UpdateView):
    model = Item
    fields = '__all__'

class ItemDelete(DeleteView):
    model = Item
    success_url = '/items/browse/'