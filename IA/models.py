from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    class OptionsCategory(models.TextChoices):
        OPTION1 = 'Weapons'
        OPTION2 = 'Potions'
        OPTION3 = 'Armors'

    class OptionsType(models.TextChoices):
        OPTION1 = 'Sword'
        OPTION2 = 'Axe'
        OPTION3 = 'Crossbow'
        OPTION4 = 'Spear'
        OPTION5 = 'Dagger'
        OPTION6 = 'Wand'

    class OptionsRarity(models.TextChoices):
        OPTION1 = 'Bronze'
        OPTION2 = 'Silver'
        OPTION3 = 'Gold'
        OPTION4 = 'Emerald'
        OPTION5 = 'Diamond'
        OPTION6 = 'Ruby'
        OPTION7 = 'Obsidian'
        OPTION8 = 'Opal'

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=20, choices=OptionsCategory.choices)
    name = models.CharField(max_length=30)
    rarity = models.CharField(max_length=20, choices=OptionsRarity.choices)
    image = models.BinaryField()
    type = models.CharField(max_length=20, choices=OptionsType.choices)
    status_card = models.IntegerField()
    power = models.IntegerField()
    description = models.CharField(max_length=500)
    serial = models.CharField(max_length=20, default="WE-000.001")

    objects = models.Manager()


class Status(models.Model):
    class OptionsStatus(models.TextChoices):
        OPTION1 = 'STR'
        OPTION2 = 'VIT'
        OPTION3 = 'RES'
        OPTION4 = 'AGI'
        OPTION5 = 'LUC'
        OPTION6 = 'INT'

    class OptionsRarity(models.TextChoices):
        OPTION1 = 'Bronze'
        OPTION2 = 'Silver'
        OPTION3 = 'Gold'
        OPTION4 = 'Emerald'
        OPTION5 = 'Diamond'
        OPTION6 = 'Ruby'
        OPTION7 = 'Obsidian'
        OPTION8 = 'Opal'

    id = models.AutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=False)
    rarity = models.CharField(max_length=20, choices=OptionsRarity.choices)
    attribute = models.CharField(max_length=10, choices=OptionsStatus.choices)
    stats = models.IntegerField()

    objects = models.Manager()


'''class Card(models.Model):

    Options_category = [(option.value, option.name) for option in OptionsCategory]
    Options_type = [(option.value, option.name) for option in OptionsType]
    Options_rarity = [(option.value, option.name) for option in OptionsRarity]

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20, choices=Options_category)
    name = models.CharField(max_length=30)
    rarity = models.CharField(max_length=20, choices=Options_rarity)
    type = models.CharField(max_length=20, choices=Options_type)
    status_card = models.IntegerField(max_digits=5)
    power = models.IntegerField(max_digits=5)
    description = models.TextField()

    def __str__(self):
        return {self.name}, {self.category}, {self.type}, {self.rarity}, {self.description}'''

'''class User(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=30)'''