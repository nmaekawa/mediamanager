from django.contrib import admin
from .models import MediaStore, Course, Collection, Resource, Item

class CollectionsInline(admin.StackedInline):
    extra = 0
    verbose_name = 'Collection'
    model = Collection

class ResourcesInline(admin.StackedInline):
    extra = 0
    verbose_name = 'Resource'
    model = Resource

class ItemsInline(admin.StackedInline):
    extra = 0
    verbose_name = 'Item'
    model = Item

class MediaStoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'file_md5hash', 'file_type', 'file_size', 'img_width', 'img_height', 'reference_count')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'lti_context_id', 'lti_tool_consumer_instance_guid')
    inlines = (ResourcesInline, CollectionsInline)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'sort_order')
    ordering = ('course', 'sort_order')
    inlines = (ItemsInline,)

admin.site.register(MediaStore, MediaStoreAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Resource)
admin.site.register(Item)
