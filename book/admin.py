from django.contrib import admin
from .models import Book
from django.utils.html import format_html
import json
from .models import WastewaterRecord


class BookAdmin(admin.ModelAdmin):
    # 리스트 뷰에 표시할 필드
    list_display = ('name', 'remain', 'reserved', 'recent_use', 'tag_list', 'image_preview')
    list_filter = ('recent_use',)
    search_fields = ('name', 'tags')
    readonly_fields = ('usage_history_formatted', 'reservation_list_formatted', 'image_preview')

    # 상세 보기에서 보여줄 필드
    fieldsets = (
        (None, {
            'fields': ('name', 'remain', 'reserved', 'recent_use', 'tags', 'content', 'img', 'image_preview')
        }),
        ('사용 기록', {
            'fields': ('usage_history_formatted',),
        }),
        ('예약 리스트', {
            'fields': ('reservation_list_formatted',),
        }),
    )

    def usage_history_formatted(self, obj):
        """사용 기록을 보기 좋게 포맷"""
        if obj.usage_history:
            formatted = json.dumps(obj.usage_history, indent=4, ensure_ascii=False)
            return format_html('<pre style="white-space: pre-wrap;">{}</pre>', formatted)
        return "사용 기록이 없습니다."
    usage_history_formatted.short_description = "사용 기록"

    def reservation_list_formatted(self, obj):
        """예약 리스트를 보기 좋게 포맷"""
        if obj.reservation_list:
            formatted = json.dumps(obj.reservation_list, indent=4, ensure_ascii=False)
            return format_html('<pre style="white-space: pre-wrap;">{}</pre>', formatted)
        return "예약 리스트가 없습니다."
    reservation_list_formatted.short_description = "예약 리스트"

    def tag_list(self, obj):
        """태그를 쉼표로 분리해서 보여주기"""
        return ", ".join([tag.strip() for tag in obj.tags.split(',')]) if obj.tags else "태그 없음"
    tag_list.short_description = "태그"

    def image_preview(self, obj):
        """이미지 필드의 미리보기"""
        if obj.img:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.img.url)
        return "이미지 없음"
    image_preview.short_description = "이미지 미리보기"


# Admin 등록
admin.site.register(Book, BookAdmin)

@admin.register(WastewaterRecord)
class WastewaterRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'date')  # 어드민 리스트에 표시할 필드
    search_fields = ('name',)  # 검색 기능
    list_filter = ('date',)  # 필터 기능 추가