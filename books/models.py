from django.db import models
from django.utils import timezone as tz
from drugs.models import Drug
from django.db.models import Q

# Create your models here.

class Credit(models.Model):
    """ Records of all crediting transactions """

    item = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(default=tz.now)

    def __str__(self) -> str:
        return f"Credit for {self.item}"


class Debit(models.Model):
    """ Records of all debiting transactions """

    item = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(default=tz.now)

    def __str__(self) -> str:
        return f"Debit for {self.item}"


class Sale(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    price = models.FloatField()
    time = models.DateTimeField(default=tz.now)

    def save(self, *args, **kwargs) -> None:
        item_set = self.drug.get_item_set() # Itemset is currently ony a single (first) item
        item_set.sell(self.amount)
        return super(Sale, self).save(*args, **kwargs)

    def rank(self, interval: int=30) -> list[Drug]:
        """  Rank drugs based on number of sales
        Params:
            interval: number of previous days to consider  """

        pass

    def top10(self, interval: int=30) -> str:
        """ Return top 10 drugs sold
        Params:
            interval: number of previous days to consider """

        pass

    def __str__(self) -> str:
        return f"Sale of {self.amount} {self.drug.name}(s)"


class Purchase(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    price = models.FloatField()
    date = models.DateField(default=tz.now)

    def __str__(self) -> str:
         return f"Purchase of {self.amount} {self.drug.name}(s) on {self.date}"


# TODO: Add cash at hand and stock at hand
class BusinessMonth(models.Model):
    " A bussiness month recording all transactions, profits or losses within the month """

    opening_cash = models.FloatField()
    opening_stock = models.IntegerField()
    opening_date = models.DateField(default=tz.now)
    closing_cash = models.FloatField(null=True)
    closing_stock = models.IntegerField(null=True)
    closing_date = models.DateField(null=True)
    # margin = models.FloatField(default=0)

    def any(self) -> bool:
        """ Check if any business month exists """

        months = BusinessMonth.objects.all()

        if months.count() != 0:
            return True
        return False

    def get_credits(self, opening: tz.datetime=None, closing: tz.datetime=None) -> models.QuerySet:
        """ Get total credits within a timeframe """

        if not opening:
            opening = self.opening_date
        if not self.closing_date:
            closing = closing
        else:
            closing = self.closing_date
        if not closing:
            closing = tz.now()

        credits = Credit.objects.filter(date__gte=opening)
        credits = credits.filter(date__lte=closing)

        return credits

    def get_credits_price(self, opening: tz.datetime=None, closing: tz.datetime=None) -> float:
        """ Get total price of credits within a timeframe """

        credit = 0

        for item in self.get_credits(opening=opening, closing=closing):
            credit += item.price
        
        return float(credit)

    def get_debits(self, opening: tz.datetime=None, closing: tz.datetime=None) -> models.QuerySet:
        """ Get total debits within a timeframe """

        if not opening:
            opening = self.opening_date
        if not self.closing_date:
            closing = closing
        else:
            closing = self.closing_date
        if not closing:
            closing = tz.now()

        debits = Debit.objects.filter(date__gte=opening)
        debits = debits.filter(date__lte=closing)

        return debits

    def get_debits_price(self, opening: tz.datetime=None, closing: tz.datetime=None) -> float:
        """ Get total price of debits within a timeframe """

        debit = 0

        for item in self.get_debits(opening=opening, closing=closing):
            debit += item.price

        return float(debit)

    def get_sales(self, opening: tz.datetime=None, closing: tz.datetime=None) -> models.QuerySet:
        """ Get total sales within a timeframe """

        if not opening:
            opening = self.opening_date
        if not self.closing_date:
            closing = closing
        else:
            closing = self.closing_date
        if not closing:
            closing = tz.now()

        # sales = Sale.objects.filter(time__date=closing.date())
        sales = Sale.objects.filter(time__gte=opening)
        sales = sales.filter(time__lte=closing)

        return sales

    def get_sales_price(self, opening: tz.datetime=None, closing: tz.datetime=None) -> float:
        """ Get total price of sales within a timeframe """

        sale = 0

        for item in self.get_sales(opening=opening, closing=closing):
            sale += item.price #com

        return float(sale)

    def get_purchases(self, opening: tz.datetime=None, closing: tz.datetime=None) -> models.QuerySet:
        """ Get total purchases within a timeframe """

        if not opening:
            opening = self.opening_date
        if not self.closing_date:
            closing = closing
        else:
            closing = self.closing_date
        if not closing:
            closing = tz.now()

        purchases = Purchase.objects.filter(date__gte=opening)
        purchases = purchases.filter(date__lte=closing)

        return purchases

    def get_purchases_price(self, opening: tz.datetime=None, closing: tz.datetime=None) -> float:
        """ Get total price of purchases within a timeframe """

        purchase = 0

        for item in self.get_purchases(opening=opening, closing=closing):
            purchase += item.price
        
        return float(purchase)

    # Same as get sales; useful?
    def get_costs(self, opening: tz.datetime=None, closing: tz.datetime=None) -> models.QuerySet:
        """ Get total costs within a timeframe """

        if not opening:
            opening = self.opening_date
        if not self.closing_date:
            closing = closing
        else:
            closing = self.closing_date
        if not closing:
            closing = tz.now()

        costs = Sale.objects.filter(time__gte=opening)
        costs = costs.filter(time__lte=closing)

        return costs

    def get_costs_price(self, opening: tz.datetime=None, closing: tz.datetime=None) -> float:
        """ Get total cost price of drugs sold within a timeframe """

        cost = 0

        for item in self.get_costs(opening=opening, closing=closing):
            cost += (item.drug.cost_price * item.amount)
        
        return float(cost)

    def balance_cash(self, opening: tz.datetime=None, closing: tz.datetime=None) -> float:
        """ Compute balance on cash """

        credits = self.get_credits_price(opening=opening, closing=closing)
        debits = self.get_debits_price(opening=opening, closing=closing)

        balance = self.opening_cash + credits - debits
        return balance

    def balance_stock(self, opening: tz.datetime=None, closing: tz.datetime=None) -> float:
        """ Compute balance on stock """

        bought = self.get_purchases_price(opening=opening, closing=closing)
        sold = self.get_sales_price(opening=opening, closing=closing)

        balance = self.opening_stock + bought - sold
        return balance

    def calculate_margins(self,opening: tz.datetime=None, closing: tz.datetime=None, commit: bool=True) -> float:
        if not closing:
            closing = self.closing_date
        if not closing:
            closing = tz.now()

        #: int: Margin on drugs sold
        sale_margin = self.get_sales_price(opening=opening, closing=closing) - self.get_costs_price(opening=opening, closing=closing)

        #: int Margin on debits and credits
        margin = self.get_credits_price(opening=opening, closing=closing) - self.get_debits_price(opening=opening, closing=closing)

        return margin, sale_margin

    def close(self, dates: str=None) -> None:
        """ Close the accounts for a month """

        self.closing_cash = self.balance_cash()
        self.closing_stock = self.balance_stock()
        self.closing_date = tz.now().date()

        if dates:
            try:
                y, m, d = dates.split("-")
                closing = tz.datetime(int(y), int(m), int(d))
                self.closing_date = closing.date()
            except Exception:
                raise ValueError(f"Invalid date: Date must be in the format 'yyyy-mm-dd' with no preceding zeros (01)")

            # self.calculate_margins()
        self.save()
    
    @property
    def margin(self) -> int:
        """ Margin based on credits and debits """

        return self.calculate_margins(closing=None)[0]

    def sale_margin(self) -> int:
        """ Margin on sales """

        return self.calculate_margins(closing=None)[1]

    def __str__(self):
        return f"Bussiness month from {self.opening_date} to {self.closing_date}"