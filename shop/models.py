from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    hashPassword = models.CharField(max_length=64)
    def __str__(self):
        return self.username

class ItemUpdated(models.Model):
    item_name = models.CharField(max_length=64)
    item_image = models.CharField(max_length=300)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.TextField()
    item_type = models.CharField(max_length=32)
    def __str__(self):
        return self.item_name    

class Bid(models.Model):
    buyerId = models.ForeignKey(User, on_delete=models.CASCADE)
    itemId = models.ForeignKey(ItemUpdated, on_delete=models.CASCADE)
    bidAmount = models.DecimalField(max_digits=10, decimal_places=2)

class ItemUserConnect(models.Model):
    userPlacedABid = models.ForeignKey(User, on_delete=models.CASCADE)
    itemGotBid = models.ForeignKey(ItemUpdated, on_delete=models.CASCADE)
    bidAdmin = models.BooleanField(default=False)



