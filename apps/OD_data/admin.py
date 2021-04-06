from django.contrib import admin
from .models import UploadRecord, OneFrameData, LabelCategory

# Register your models here.

@admin.register(UploadRecord)
class UploadRecordAdmin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ('title', 'run_time', 'data_size', 'upload_time',)
    # 需要搜索的字段
    search_fields = ('title', )

    list_filter = ('data_size', 'upload_time',)

@admin.register(OneFrameData)
class OneFrameDataAdmin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ('annotation',)
    # 需要搜索的字段
    search_fields = ('annotation',)


@admin.register(LabelCategory)
class LabelCategoryAdmin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ('category',)
