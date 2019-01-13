from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    deposit = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(max_length=100)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {} ({})'.format(
            self.room_number, self.room_type, self.room_type.cost)


class CompanyAccount(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Guest(models.Model):
    SELECT = 0
    FEMALE = 1
    MALE = 2
    SEXES = enumerate(('Select', 'Female', 'Male'))

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    deposit = models.DecimalField(decimal_places=2, max_digits=10)
    surname = models.CharField(max_length=200)
    other_names = models.CharField(max_length=200)
    sex = models.PositiveIntegerField(choices=SEXES, default=0)
    nationality = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    car_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    purpose = models.CharField(max_length=20, blank=True)
    arriving_from = models.CharField(max_length=20, blank=True)
    travelling_to = models.CharField(max_length=20, blank=True)
    passport_no = models.CharField(max_length=20, blank=True)
    arrival_date = models.DateField(default=timezone.now)
    departure_date = models.DateField(null=True, blank=True)
    account = models.ForeignKey(CompanyAccount, null=True, blank=True, on_delete=models.SET_NULL)
    num_adults = models.IntegerField()
    num_children = models.IntegerField()
    checked_out = models.BooleanField(default=False)

    def __str__(self):
        return self.surname

    @property
    def full_name(self):
        return '{} {}'.format(self.other_names, self.surname)

    class Meta:
        ordering = ["-id", "-arrival_date"]


class Facility(models.Model):
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Booking(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    booked_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.facility)


class HouseKeeping(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class RequisitionMaster(models.Model):
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class Requisition(models.Model):
    item = models.ForeignKey(HouseKeeping, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    master = models.ForeignKey(RequisitionMaster, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return unicode(self.item)


class Bill(models.Model):
    RESTAURANT = 0
    MAIN_BAR = 1
    SWIMMING_POOL_BAR = 2
    LAUNDRY = 3
    GYM = 4
    SERVICES = enumerate(
        ('Restaurant', 'Main Bar', 'Pool Bar', 'Laundry', 'Gym'))

    guest = models.ForeignKey(Guest, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    bill_date = models.DateField(default=timezone.now)
    paid = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    service = models.PositiveIntegerField(choices=SERVICES)

    def __str__(self):
        return '{}'.format(self.amount)

    @property
    def pending(self):
        return not self.paid


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    RESTAURANT = 0
    MAIN_BAR = 1
    SWIMMING_POOL_BAR = 2
    STORE = 3
    SELECT = 4
    LOCATIONS = enumerate(
        ('Restaurant', 'Main Bar', 'Pool Bar', 'Store', 'Select Location'))

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    location = models.PositiveIntegerField(choices=LOCATIONS, default=4)

    def __str__(self):
        return unicode(self.item)


class PurchaseMaster(models.Model):
    when = models.DateField(default=timezone.now)

    def __str__(self):
        return self.when.strftime('%d-%m-%Y')


class Purchase(models.Model):
    master = models.ForeignKey(PurchaseMaster, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return unicode(self.inventory)

    @property
    def total(self):
        return self.quantity * self.price


class Transfer(models.Model):
    RESTAURANT = 0
    MAIN_BAR = 1
    SWIMMING_POOL_BAR = 2
    LOCATIONS = enumerate(
        ('Restaurant', 'Main Bar', 'Pool Bar'))

    destination = models.PositiveIntegerField(choices=LOCATIONS)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    when = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.destination, self.item)
