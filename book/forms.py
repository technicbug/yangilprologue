from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'remain', 'tags', 'content', 'img']  # 수정 가능한 필드
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'remain': forms.NumberInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'img': forms.FileInput(attrs={'class': 'form-control'}),  # 이미지 업로드 필드 추가
        }
