from .forms import NoteAddForm
from .models import Note, NotedModel
from foods.models import Dish, Order
from decimal import Decimal
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.db.models import Q


def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', context={'notes': notes})


def note_search(request):
    query = request.GET['query']
    if query:
        notes = Note.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return render(request, 'notes/note_list.html', context={'notes': notes})


def note_add(request):
    if request.user.has_perm('notes.add_note'):
        if request.method == "POST":
            dish_id = request.POST.get("noted_dish_select")
            order_id = request.POST.get("noted_order_select")
            if dish_id:
                model_instance = Dish.objects.get(id=dish_id)
            if order_id:
                model_instance = Order.objects.get(id=order_id)

            form = NoteAddForm(request.POST, request.FILES)
            if form.is_valid():
                new_note = form.save()
                NotedModel.objects.create(content_object=model_instance, note=new_note)

                return HttpResponseRedirect(reverse('note_list'))

        form = NoteAddForm()
        dishes = Dish.objects.all()
        orders = Order.objects.all()

        return render(request, 'notes/note_add.html', context={'form': form, 'dishes': dishes, 'orders': orders})
    else:
        request.session['permission_codename'] = 'add_note'
        return HttpResponseRedirect(reverse('permission_denied'))


def note_view(request, note_id):
    note = Note.objects.get(id=note_id)
    try:
        noted_model = NotedModel.objects.get(note__id=note.id)
    except NotedModel.DoesNotExist:
        noted_model = None

    model_instance = None
    model_instance_class = None
    if noted_model:
        model_instance = noted_model.content_object.__class__.objects.get(id=noted_model.content_object.id)
        model_instance_class = str(noted_model.content_object.__class__.__name__.lower())

    if note:
        return render(request, 'notes/note_view.html', context={'note': note, 'model_instance': model_instance,
                                                                'model_instance_class': model_instance_class})


def note_edit(request, note_id):
    if request.user.has_perm('notes.change_note'):
        note = Note.objects.get(id=note_id)
        if note:

            if request.method == "POST":
                dish_id = request.POST.get("noted_dish_select")
                order_id = request.POST.get("noted_order_select")
                model_instance = None
                if dish_id:
                    model_instance = Dish.objects.get(id=dish_id)
                if order_id:
                    model_instance = Order.objects.get(id=order_id)

                form = NoteAddForm(request.POST, request.FILES, instance=note)
                if form.is_valid():
                    edit_note = form.save()
                    NotedModel.objects.filter(note__id=edit_note.id).delete()
                    NotedModel.objects.create(content_object=model_instance, note=edit_note)

                    return HttpResponseRedirect(reverse('note_list'))

            form = NoteAddForm()
            dishes = Dish.objects.all()
            orders = Order.objects.all()
            try:
                noted_model = NotedModel.objects.get(note__id=note.id)
            except NotedModel.DoesNotExist:
                noted_model = None
            dish_id = dish_select_disabled = dish_select_required = None
            order_id = order_select_disabled = order_select_required = None

            if noted_model:
                if noted_model.content_object.__class__.__name__ == 'Dish':
                    dish_id = noted_model.content_object.id
                    order_id = None
                    dish_select_disabled = False
                    dish_select_required = True
                    order_select_disabled = True
                    order_select_required = False
                if noted_model.content_object.__class__.__name__ == 'Order':
                    order_id = noted_model.content_object.id
                    dish_id = None
                    dish_select_disabled = True
                    dish_select_required = False
                    order_select_disabled = False
                    order_select_required = True

            return render(request, 'notes/note_edit.html',
                          context={'note': note,
                                   'form': form,
                                   'dishes': dishes,
                                   'orders': orders,
                                   'dish_id': dish_id,
                                   'order_id': order_id,
                                   'dish_select_disabled': dish_select_disabled,
                                   'dish_select_required': dish_select_required,
                                   'order_select_disabled': order_select_disabled,
                                   'order_select_required': order_select_required,

                                   })
    else:
        request.session['permission_codename'] = 'change_note'
        return HttpResponseRedirect(reverse('permission_denied'))


def note_delete(request, note_id):
    if request.user.has_perm('notes.delete_note'):
        note = Note.objects.get(id=note_id)

        if note:
            if request.method == "POST":
                note.delete()
                return HttpResponseRedirect(reverse('note_list'))
    else:
        request.session['permission_codename'] = 'delete_note'
        return HttpResponseRedirect(reverse('permission_denied'))
