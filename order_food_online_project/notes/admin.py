from django.contrib import admin
from .models import NotedModel, Note
from django.contrib.contenttypes.admin import GenericTabularInline

class NotedModelInline(GenericTabularInline):
    model = NotedModel


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_on')
    list_filter = ('title',)
    search_fields = ('title', 'description', 'created_on')
    inlines = [
        NotedModelInline,
    ]


class NotedModelAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'content_object', 'note_title', 'note_description', 'note_created_on')
    list_filter = ('content_type',)
    search_fields = ('content_type', 'object_id', 'content_object',)


    def note_title(self, obj):
        return obj.note.title

    def note_description(self, obj):
        return obj.note.description

    def note_created_on(self, obj):
        return obj.note.created_on


admin.site.register(Note, NoteAdmin)
admin.site.register(NotedModel, NotedModelAdmin)
