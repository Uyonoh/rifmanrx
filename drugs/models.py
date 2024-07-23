from typing import Iterable
from django.db import models
from django.utils import timezone as tz

# Create your models here.

# Choices for drug state
state_choices = (("Tab", "Tab"), ("Suspension", "Suspension"), ("Injectable", "Injectable"))

# Choices for purchase units
unit_choices = (("Cartons", "Cartons"), ("Packets", "Packets"), ("Unit", "Sachets/Bottle/Card"))


class Drug(models.Model):
    """ Base drug class """

    name = models.CharField(max_length=30)
    brand_name = models.CharField(max_length=30)
    mass = models.CharField(max_length=10)
    state = models.CharField(max_length=10, choices=state_choices, default="Tablet")
    manufacturer = models.CharField(max_length=30)
    exp_date = models.DateField("Expiery Date")
    stock_amount = models.IntegerField(null=True)
    purchase_amount = models.IntegerField()
    purchase_units = models.CharField(max_length=30, choices=unit_choices, default="Unit")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30)
    purpose = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    day_added = models.DateField(null=False, default=str(tz.now().date))
    oos = models.BooleanField(default=False) # Out of stock
    

    def check_exp(self) -> int:
        """ Returns an integer indicating the number of days till a drug is expired"""

        diff = self.exp_date - tz.now().date()
        days = diff.days
        return days
    
    def check_oos(self) -> bool:
        """ Check if a drug is out of stock """

        return self.stock_amount <= 0
    
    def clean_stock(self) -> int | str:
        """ Cleans stock for tablets
         
          Recalculate stock for tablets based on its' number
          of cards and tablets per pack

          Returns stock amount if not tablet
        """

        if self.state == "Tab":
            cd, tab = self.Tablet.get_cd_tab()
            cd, tab = int(cd), int(tab)

            amount = self.stock_amount / tab

            if amount < 1:
                amount = str(self.stock_amount) + "tab(s)"

            return amount

        return self.stock_amount
    
    def exists(self) -> models.Model:
        """ Check if drug instance already exists """

        drug = Drug.objects.filter(
            name=self.name,
            mass=self.mass,
            exp_date=self.exp_date
            )
        
        return drug.count() > 0
    

    def export(self) -> models.Model:
        """ Return drug instance """

        drug = Drug.objects.filter(
            name=self.name,
            mass=self.mass,
            exp_date=self.exp_date
            )
        
        return drug[0]
    
    @property
    def expired(self) -> bool:
        """ Expired property of drug """

        return self.check_exp() <= 0
    
    @property
    def expire_soon(self, days: int=60) -> bool:
        """ Check if drug is soon to expire.

        Args:
            days:
                Number of days considered as soon to expire
           """
        
        return self.check_exp() <= days
    
    @property
    def exp_class(self) -> str:
        """ Returns a string to be used as a class for viewing drugs in a table """

        if self.expired:
            return "expired"
        
        if self.expire_soon:
            return "exp-soon"
        
        return "exp-far"
    
    def get_unit(self) -> str:
        """ Get the base purchase unit of the drug """

        if self.state == "Tab":
            return "card(s)"
        else:
            return "bottle(s)"

    def get_item_set(self) -> models.QuerySet:
        """ Return the item set of a tablet, suspension, or injectible """

        try:
            return self.Tablet
        except AttributeError:
            pass

        try:
            return self.Suspension
        except AttributeError:
            pass

        try:
            return self.Injectible
        except AttributeError:
            raise RuntimeError("An error seems to occured with this drug!")

    def itemize(self) -> list:

        return list(zip(self.table_head(), self.tabulate()))
        
    def relocate(self, new_location: str) -> None:
        """ Change location of drug """

        self.location = new_location
        self.save()

# Not in use?
    def set_amount(self) -> None:
        """ Set stock amount for drug """

        no_cd, no_tab = self.Tablet.get_cd_tab()
        self.stock_amount = self.purchase_amount * int(no_tab)

        if self.units == "Unit":
            self.stock_amount *= int(no_cd) 

        if self.units == "Cartons":
            self.stock_amount = self.stock_amount * self.no_packs

# Check it again
    def sell(self, amount: int, is_tab: bool):
        """ Sell the drug
         
        Subtracts amount from stock """

        self.stock_amount -= amount

        self.validate_stock_amount(amount)
        self.save(first_stock=False, sale=True)

    def table_head(self) -> tuple:
        return ("name", "brand name", "state", "mass", "manufacturer", "Expirery date", "stock", "price",
                "category", "Out of stock", "expired")

    def tabulate(self) -> tuple:
        """ Returns a tuple of some drug attributes to be used a table """

        return (self.name, self.brand_name, self.state, self.mass,
			    self.manufacturer, self.exp_date, self.clean_stock(), self.price, self.category,
			    self.oos, self.expired)
    
    def validate_stock_amount(self, amount: int=0) -> None:
        """ Ensure stock amount is not less than zero """

        if self.stock_amount < 0:
            raise ValueError(f"amount {amount} greater than stock amount")
    
    @property
    def Tablet(self) -> models.Model:
        """ Gets the tablet assossiated with the drug 
        
        There should only be one"""

        # TODO: link all drugs with same name, using differernt tablets

        return self.tablet_set.all()[0]

    @property
    def Suspension(self) -> models.Model:
        """ Gets the suspension assossiated with the drug """
        
        return self.suspension_set.all()[0]

    @property
    def Injectible(self) -> models.Model:
        """ Gets the suspension assossiated with the drug """

        return self.injectible_set.all()[0]
    
    def __str__(self) -> str:
        return f" {self.name} Tablet: A drug for {self.purpose} located at {self.location}.\
                Expires: {self.exp_date} "


class Tablet(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    cd_tab = models.CharField(max_length=10, null=True)
    no_packs = models.IntegerField(null=True, default=0)

    def get_cd_tab(self) -> list:
        """ Splits cd_tab using '/' """

        return self.cd_tab.split("/")
    
    def set_amount(self, units: str=None, amount: int=None) -> int:
        """ Recalculate purchase amount based on purchase units """

        no_cd, no_tab = self.get_cd_tab()

        if amount:
            self.drug.purchase_amount = amount

        if units:
            self.drug.purchase_units = units

        amount = self.drug.purchase_amount * int(no_tab) # Units=unit

        if self.drug.purchase_units == "Packets":
            amount *= int(no_cd)

        if self.drug.purchase_units == "Cartons":
            amount = amount * self.no_packs * int(no_cd)

        return amount
    
    # TODO: Enable on-the -fly edits of prices
    def set_price(self, price: int=None) -> int:
        """ Set the price of drug based on purchase units and return price """

        # If price is not supplied, set to cost price
        if not price:
            price = self.drug.cost_price
        # Price per purchase unit
        price = price / self.drug.purchase_amount

        # If purchase unit is packet, div by no of cards in pack.
        # Further div by no of packs in carton if unit is carton
        if self.drug.purchase_units == "Packets":
            price = price / int(self.get_cd_tab()[0])
        elif self.drug.purchase_units == "Cartons":
            price = price / self.no_packs
            price = price . int(self.get_cd_tab()[0])

        # Set cost price to cost price per unit
        self.drug.cost_price = price
        # Set sale price to cost price per unit
        self.drug.price = price

        return price
    
    def sell(self, amount: int, units: str="units", is_tab: bool=False) -> None:
        """ Sell tablet """

        if is_tab:
            self.drug.stock_amount -= amount
        else:
            no_cd, no_tab = self.get_cd_tab()
            amount = amount * int(no_tab)

            if units == "Packets":
                amount *= int(no_cd)
            elif units == "Cartons":
                amount *= int(no_cd)
                amount *= self.no_packs
        
            self.drug.stock_amount -= amount
            self.drug.validate_stock_amount(amount)
        self.drug.save()

    def save(self, price: int=None, units: str=None, amount: int=None, first_stock: bool=True, update: bool=False, sale: bool=False, drug_update_fields: list=None, **kwargs):
        
        # If not selling, then it must be addition of stock
        # If price is passed, then it must be an update
        if price:
            update = True
        # Set/update price
        
        stock = self.set_amount(units, amount)

        if update:
            stock += self.drug.stock_amount

        self.drug.stock_amount = stock

        if not sale:
            self.set_price(price)
        self.drug.save(update_fields=drug_update_fields)

        if not update:
            return super(Tablet, self).save(**kwargs)
    
    def update_stock(self) -> None:
        pass

    def __str__(self) -> str:
        return f" {self.drug.name} Tablet: A drug for {self.drug.purpose} located at {self.drug.location}.\
                Expires: {self.drug.exp_date} "
    
    @property
    def card_price(self) -> int:
        """ Returns the price per card """

        return self.drug.price
    
    @property
    def tab_price(self) -> int:
        """ Returns the price per tablet """

        no_tab = self.get_cd_tab()[1]
        no_tab = int(no_tab)
        
        price = self.card_price / no_tab
        return price
    
    @property
    def ntabs(self) -> int:
        """ Return the number of tabs per card """

        return int(self.get_cd_tab()[1])
    
    @property
    def ncards(self) -> int:
        """ Return the number of cards per pack """

        return int(self.get_cd_tab()[0])
    
    @property
    def pack_price(self) -> int:
        """ Returns the price per pack """

        return self.card_price * self.ncards
    
    @property
    def carton_price(self) -> int:
        """ Return the price per carton """

        return self.pack_price * self.no_packs
    
    @property
    def stock_cards(self) -> int:
        """ Return the number of cards in stock """

        return self.drug.stock_amount / self.ntabs

class Suspension(models.Model):
    pass

class Injectible(models.Model):
    pass


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