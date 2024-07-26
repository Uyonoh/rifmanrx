from django.db import models
from django.utils import timezone as tz
from drugs.models import Drug

# Create your models here.

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