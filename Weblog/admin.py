from django.contrib import admin

from Weblog.models import Weblog, Category, Tag, Comment, CommentLike


@admin.register(Weblog)
class WeblogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CommentLikeAdmin(admin.StackedInline):
    model = CommentLike
    extra = 1
    can_delete = False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent', 'created_at', 'updated_at')

    inlines = [CommentLikeAdmin]
