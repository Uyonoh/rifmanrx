from django.db import models
from django.utils import timezone as tz
from drugs.models import Drug

# Create your models here.

class Credit(models.Model):
    """ Records of all crediting transactions """

    item = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(default=tz.now().date)

    def __str__(self) -> str:
        return f"Credit for {self.item}"


class Debit(models.Model):
    """ Records of all debiting transactions """

    item = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(default=tz.now().date)

    def __str__(self) -> str:
        return f"Debit for {self.item}"


class Sale(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.FloatField()
    time = models.DateTimeField(default=tz.now)

    def save(self, *args, **kwargs) -> None:
        item_set = self.drug.get_item_set() # Itemset is currently ony a single (first) item
        item_set.sell(self.amount)
        return super(Sale, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Sale of {self.amount} {self.drug.name}(s) on {self.time.date()} at {self.time.time()}"
    

class Purchase(models.MOdel):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(default=tz.now().date)

    def __str__(self) -> str:
         return f"Purchase of {self.amount} {self.drug.name}(s) on {self.date}"