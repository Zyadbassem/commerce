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

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemUpdated, on_delete=models.CASCADE)  


class FinishBids(models.Model):
    lastBid = models.DecimalField(decimal_places=3,max_digits=10)
    buyer = models.ForeignKey(User, related_name='bought_bids', on_delete=models.CASCADE, default=1)
    seller = models.ForeignKey(User, related_name='sold_bids', on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(ItemUpdated, on_delete=models.CASCADE)



