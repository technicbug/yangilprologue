from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 약품 목록 및 검색
    path("chemicals/", views.chemical_list, name="chemical_list"),  # URL 경로 수정 및 명확한 네이밍

    # 약품 예약
    path("reserve/", views.reservation_view, name="reservation_view"),  # 예약 경로 추가
    path('<int:pk>/', views.chemical_detail, name='chemical_detail'),  # 약품 상세 정보 페이지
    path('manage/', views.manage_chemicals, name='manage_chemicals'),  # 약품 관리 페이지
    path('update/<int:pk>/', views.update_chemical, name='update_chemical'),  # 약품 수정
    path('delete/<int:pk>/', views.delete_chemical, name='delete_chemical'),  # 약품 삭제
    path('cancel/<int:pk>/', views.cancel_reservations, name='cancel_reservation'),  # 예약 취소

    path('wastewater/', views.wastewater_page, name='wastewater_page'),
    path('wastewater/record/', views.record_wastewater, name='record_wastewater'),

    path('molcalc/', views.molcalc, name='mol_calc')
]
