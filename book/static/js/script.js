// 테이블에서 예약 폼을 보여주는 함수
function showReservationFormTable(chemicalId) {
    const form = document.getElementById('reservation-form-table-' + chemicalId);
    if (form) {
        form.style.display = 'block';
    }
    document.querySelector('[data-id="' + chemicalId + '"]').style.display = 'none';
}

// 테이블에서 예약 폼을 숨기는 함수
function hideReservationFormTable(chemicalId) {
    const form = document.getElementById('reservation-form-table-' + chemicalId);
    if (form) {
        form.style.display = 'none';
    }
    document.querySelector('[data-id="' + chemicalId + '"]').style.display = 'inline-block';
}

// 카드에서 예약 폼을 보여주는 함수
function showReservationFormCard(chemicalId) {
    const form = document.getElementById('reservation-form-card-' + chemicalId);
    if (form) {
        form.style.display = 'block';
    }
    document.querySelector('[data-id="' + chemicalId + '"]').style.display = 'none';
    
}

// 카드에서 예약 폼을 숨기는 함수
function hideReservationFormCard(chemicalId) {
    const form = document.getElementById('reservation-form-card-' + chemicalId);
    if (form) {
        form.style.display = 'none';
    }
    document.querySelector('[data-id="' + chemicalId + '"]').style.display = 'inline-block';
}

$(document).ready(function () {
    // 토글 버튼 클릭 시 메뉴 표시/숨기기
    $('.navbar-toggler').on('click', function () {
        $('#tm-header').toggleClass('show');
    });
});