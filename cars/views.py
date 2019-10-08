from django.shortcuts import render, redirect
from .models import Car
from .forms import CarForm
from django.contrib import messages
from django.db.models import Q

def car_list(request):
    cars = Car.objects.all()
    query = request.GET.get("q")

    if query:
    	cars = cars.filter(
    		Q(make__icontains=query)|
    		Q(model__icontains=query)|
    		Q(year__icontains=query)
    		).distinct()

    context = {
        "cars": cars,
    }
    return render(request, 'car_list.html', context)


def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    context = {
        "car": car,
    }
    return render(request, 'car_detail.html', context)


def car_create(request):
    form = CarForm()
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile created.')
            return redirect('car-list')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)


def car_update(request, car_id):
    car_obj = Car.objects.get(id=car_id)
    form = CarForm(instance=car_obj)
    if request.method == "POST":
        form = CarForm(request.POST,request.FILES, instance=car_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('car-list')
    context = {
        "car_obj": car_obj,
        "form":form,
    }
    return render(request, 'update.html', context)


def car_delete(request, car_id):
    car_obj = Car.objects.get(id=car_id)
    car_obj.delete()
    messages.success(request, 'Profile deleted.')
    return redirect('car-list')