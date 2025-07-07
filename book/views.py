from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from .models import Book
from django.utils.timezone import now
from django.db.models import Q
from .forms import BookForm
from django.views.generic.edit import FormView
from django.conf import settings
from django.http import JsonResponse
from .models import WastewaterRecord
from django.db.models import Sum
from django.utils.timezone import make_aware
from django.utils.timezone import localtime
# Create your views here.

def chemical_list(request):
    query = request.GET.get("q", "")  # 검색어 가져오기
    if query:
        books = Book.objects.filter(
            Q(name__icontains=query) | Q(tags__icontains=query)
        )
    else:
        books = Book.objects.all()

    # 최근 사용 날짜와 지난 예약 정리
    for book in books:
        book.process_past_reservations()

    return render(request, "book/book.html", {"books": books, "query": query})

def reservation_view(request):
    if request.method == "POST":
        # POST 요청에서 데이터 가져오기
        book_id = request.POST.get("chemical_name")
        quantity = float(request.POST.get("quantity", 0))
        reservation_date = request.POST.get("reservation_date")
        reserver_name = request.POST.get("reserver_name", "")  # 예약자 명

        # 해당 약품 가져오기
        book = get_object_or_404(Book, id=book_id)

        # 예약 가능 최대값 계산
        max_reservable = book.remain - book.reserved

        # 예약 가능 여부 확인
        if quantity > max_reservable:
            return HttpResponse(
                f"예약량이 허용 범위를 초과했습니다. 최대 예약 가능량은 {max_reservable:.2f}입니다.", 
                status=400
            )

        # 예약 기록 추가 (usage_history에 추가)
        # new_usage_record = {
        #     "name": reserver_name,  # 예약자 명
        #     "quantity": quantity,
        #     "reservation_date": reservation_date,
        #     "comments": request.POST.get("comments", "")  # 비고
        # }
        # book.usage_history.append(new_usage_record)

        # 예약 리스트에 추가
        reservation_record = {
            "name": reserver_name,
            "quantity": quantity,
            "reservation_date": reservation_date,
            "comments": request.POST.get("comments", "")  # 비고
        }
        book.reservation_list.append(reservation_record)

        # 예약량 업데이트
        # book.remain -= quantity
        book.reserved = max(book.reserved + quantity, 0)  # 예약량 증가, 최소 0 유지

        # 마지막 사용 날짜를 업데이트
        book.recent_use = max(
            (date.fromisoformat(record["reservation_date"]) for record in book.usage_history),
            default=None
        )

        # 예약 처리 후 저장
        book.save()

        return redirect('chemical_detail', pk=book.id)  # 성공 후 목록 페이지로 리다이렉트

    return HttpResponse(status=405)  # POST가 아닌 요청에 대해 405 오류 반환


def chemical_detail(request, pk):
    # 약품 객체 가져오기
    book = get_object_or_404(Book, pk=pk)

    # 지난 예약 정리
    book.process_past_reservations()

    # usage_history 업데이트
    # for reservation in book.reservation_list:
    #     if reservation not in book.usage_history:
    #         book.usage_history.append(reservation)

    # 예약량이 음수가 되지 않도록 처리
    book.reserved = max(book.reserved, 0)

    # 최대 예약 가능량 계산
    max_reservable = book.remain - book.reserved
    print(max_reservable)

    # 이미지 경로 설정 (기본 이미지로 대체)
    default_img_url = "{% static 'img/chemical.png' %}"
    img_url = book.img.url if book.img else default_img_url

    book.save()

    # 템플릿 렌더링
    return render(
        request,
        "detail/detail.html",
        {
            "book": book,
            "max_reservable": max_reservable,
            "image_url": img_url,
        },
    )

def manage_chemicals(request):
    if request.method == 'POST':
        # 새로운 약품 추가
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_chemicals')
    else:
        form = BookForm()

    books = Book.objects.all()
    return render(request, 'edit/edit.html', {
        'books': books,
        'form': form,
    })

def update_chemical(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manage_chemicals')
    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'})

def delete_chemical(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('manage_chemicals')

def cancel_reservations(request, pk):
    if request.method == "POST":
        book = get_object_or_404(Book, pk=pk)
        book.reservation_list = []  # 예약 리스트를 비웁니다
        book.reserved = 0  # 예약량 초기화
        book.save()
        return redirect('manage_chemicals')
    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'}, status=400)

def wastewater_page(request):
    today = localtime(now())
    week_start = today - timedelta(days=today.weekday())  # 이번 주 시작일
    month_start = today.replace(day=1)  # 이번 달 시작일

    # 주간 및 월간 폐수량 계산
    weekly_wastewater = WastewaterRecord.objects.filter(date__gte=week_start).aggregate(Sum('quantity'))['quantity__sum'] or 0
    monthly_wastewater = WastewaterRecord.objects.filter(date__gte=month_start).aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_wastewater = WastewaterRecord.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0

    records = WastewaterRecord.objects.all().order_by('-date')  # 기록 목록

    context = {
        'weekly_wastewater': weekly_wastewater,
        'monthly_wastewater': monthly_wastewater,
        'total_wastewater': total_wastewater,
        'records': records,
    }
    return render(request, 'waste/waste_water.html', context)

def record_wastewater(request):
    if request.method == "POST":
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        if name and quantity:
            # 타임존 적용
            date = make_aware(datetime.now())
            WastewaterRecord.objects.create(name=name, quantity=quantity, date=date)
        return redirect('wastewater_page')
    return render(request, 'book/wastewater.html')

def molcalc(request):
    return render(request, 'mol_calc/mol_calc.html')