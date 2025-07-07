from django.db import models
from datetime import date
from django.utils.timezone import make_aware

class Book(models.Model):
    name = models.CharField(max_length=20, verbose_name="약품 이름", blank=False)
    remain = models.FloatField(verbose_name="잔여량")
    reserved = models.FloatField(verbose_name="예약량", default=0.0)
    usage_history = models.JSONField(default=list, verbose_name="사용 기록")  # 사용 기록과 예약 내역을 통합 관리
    reservation_list = models.JSONField(default=list, verbose_name="예약 리스트")  # 새로운 예약 리스트 필드 추가
    recent_use = models.DateField(blank=True, null=True, default=None)
    content = models.TextField(verbose_name="내용 설명", blank=True, null=True)
    img = models.ImageField(upload_to='books/images/', verbose_name="이미지", blank=True, null=True)
    tags = models.TextField(default='', blank=True, verbose_name='태그')

    def __str__(self):
        return self.name

    def process_past_reservations(self):
        today = date.today()
        updated_reservation_list = []
        for reservation in self.reservation_list:
            reservation_date = reservation.get("reservation_date")
            if reservation_date:
                # 문자열 날짜를 date 객체로 변환
                reservation_date_obj = date.fromisoformat(reservation_date)
                if reservation_date_obj < today:
                    # 처리된 예약을 사용 기록에 추가
                    self.usage_history.append(reservation)
                    # 잔여량 감소, 예약량 감소 (음수 방지)
                    self.remain = max(self.remain - reservation.get("quantity", 0), 0)
                    self.reserved = max(self.reserved - reservation.get("quantity", 0), 0)
                else:
                    # 유효한 예약만 유지
                    updated_reservation_list.append(reservation)

        # 예약 리스트 업데이트
        self.reservation_list = updated_reservation_list

        # 마지막 사용 날짜 업데이트
        self.recent_use = max(
            (date.fromisoformat(r["reservation_date"]) for r in self.usage_history if "reservation_date" in r),
            default=None,
        )

        # 저장
        self.save()




class WastewaterRecord(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.date and not self.date.tzinfo:  # naive datetime인지 확인
            self.date = make_aware(self.date)  # 타임존 추가
        super().save(*args, **kwargs)

