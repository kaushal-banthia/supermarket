from django.db import models

class Product(models.Model):
    name = models.CharField(max_length = 100)
    cost_price = models.FloatField()
    quantity = models.PositiveIntegerField()
    selling_price = models.FloatField()

    def __str__(self):
        return self.name
