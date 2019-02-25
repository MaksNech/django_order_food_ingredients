from .forms import NoteAddForm
from .models import Note, NotedModel
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
            form = NoteAddForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('note_list'))

        form = NoteAddForm()

        return render(request, 'notes/note_add.html', context={'form': form})
    else:
        request.session['permission_codename'] = 'add_note'
        return HttpResponseRedirect(reverse('permission_denied'))


def note_view(request, note_id):
    note = Note.objects.get(id=note_id)
    if note:
        return render(request, 'notes/note_view.html', context={'note': note})


def note_edit(request, note_id):
    if request.user.has_perm('notes.change_note'):
        note = Note.objects.get(id=note_id)
        if note:

            if request.method == "POST":
                form = NoteAddForm(request.POST, request.FILES, instance=note)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('note_list'))

            form = NoteAddForm()

            return render(request, 'notes/note_edit.html', context={'note': note, 'form': form})
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
