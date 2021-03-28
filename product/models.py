from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length = 100)
    cost_price = models.FloatField(validators=[MinValueValidator(0.0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    selling_price = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return self.name
