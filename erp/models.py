from accounts.models import AccountsModel
from django.db import models
from django.conf import settings

# Create your models here.


# model.py
class Product(models.Model):
    class Meta:
        db_table = "product"
    # """
    # 상품 모델입니다.
    # 상품 코드, 상품 이름, 상품 설명, 상품 가격, 사이즈 필드를 가집니다.
    # """
    author = models.ForeignKey(AccountsModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1)

    # """
    # choices 매개변수는 Django 모델 필드에서 사용하는 매개변수 중 하나로
    # 해당 필드에서 선택 가능한 옵션을 지정하는 역할을 합니다.
    # 변수를 통해 튜플 리스트를 받으면 첫번째 요소는 실제 DB에 저장되는 값이 되고,
    # 두번째 요소는 사용자가 볼 수 있는 레이블(옵션의 이름)이 됩니다.
    # """

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        # stock_quantity = models.IntegerField(default=0)
        if not self.pk:                 # 객체가 생성될 때
            self.stock_quantity = 0     # stock_quantity를 0으로 초기화
        super().save(*args, **kwargs)   # 이걸 써야 확실하게 저장이 된다던데???
        pass


class Inbound(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    inbound_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)

    class Meta:
        db_table = "stock"
        # 내림차순으로 정렬
        ordering = ['-inbound_date']
