요구사항
파이썬 3.8.6
django

계정 accounts
상품리스트, 입고, 출고, 창고 erp

accounts = AbstractUser를 상속받아 썼음. // form 안씀.
erp = 과제의 요구사항을 최대한 반영해서 form을 씀.

이번 과제에서는 모두 구현을 하고,
최대한 여러 방법을 활용하고,
장고의 여러 기능 들을 둘러 보며 쓰는 것에 초점을 두었다.

--prototype2--
blossom fall 2번째를 적용했다.

blossom fall을 쓰기 위해 js를 썼으며,

settings.py의 static 폴더에 css,images,js를 어떻게 써야하는지 대략적으로 알게 되었다.

'상품 출고' 링크 버튼 위치 = 상품 리스트 >>> Inventory

테스트 id  = june
비밀번호   = june

데이터베이스 초기화
python manage.py flush

--blossom prototype3--
js안에서는 장고의 static 경로를 쓸 수 없으므로
html에서 js를 불러오는 코드 안에 data-static-url="{% static 'imgs/' %}"를 넣고
js에서
const STATIC_URL = document.querySelector('script[src$="blossom2.js"]').dataset.staticUrl;
를 써서
`${STATIC_URL}petal.png`; 이라는 정적 경로를 가져올 수 있었다.

주소가 바뀔 때마다 html에서 경로를 바꿔서 주기 때문에
어디서나 가능하다.. 후...
