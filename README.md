# [프롤로그] 시약장 관리 웹
학교 시약장 웹 서버의 원본 소스코드 입니다
보안상의 이유로 settings.py 의 secret_key 부분은 삭제하였습니다. secret_key는 pythonanywhere의 파일에서 확인해주시면 감사하겠습니다.
원본 코드 손상등의 이유로 secret_key가 필요하다면 환주T를 통해 저에게 연락주시면 키를 전달해드리겠습니다.

해당 프로젝트는 Python Django를 통해 제작되었습니다.
서버는 pythonanywhere 무료계정을 통해 운영되고 있기 때문에 사진 업로드에 제한이 있을수 있으며 반드시 3개월마다 한번씩 꼭 로그인을 해서 갱신을 해주셔야 합니다.
이 코드를 사용할때는 반드시 pyenv를 통해 가상환경을 구성해주십시오.

pip list 를 출력한 결과입니다. 해당 버전의 라이브러리를 설치하여 사용해주십시오.
|라이브러리|버전|
|------|---|
|asgiref|3.7.2|
|Django|3.2.25|
|Pillow|9.5.0|
|pip|22.1.2|
|pytz|2024.2|
|setuptools|62.6.0|
|sqlparse|0.4.4|
|typing_extensions|4.7.1|
|wheel|0.37.1|

           

Admin 페이지에 접속하여 더욱 세부적인 부분까지 관리가 가능합니다.
접속법은 https://yangilprologue.pythonanywhere.com/admin/ 로 접속하시면 됩니다.
ID는 yangilprologue 이며 비밀번호는 구글계정 비밀번호와 동일합니다.

언제든지 해당 서비스 운영에 문제가 생기면 환주T를 통해 저에게 연락을 주세요. 최대한 답변드리겠습니다.

개발 : 김비오
2025년 7월 7일

