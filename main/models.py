from django.db import models


class Season(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"


class Club(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='clubs/images/')
    president = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)
    found_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class PlayersFilterManager(models.Manager):
    def get_queryset(self):
        return super(PlayersFilterManager, self).get_queryset().filter(age__lte=20)


class Player(models.Model):

    class Position(models.TextChoices):
        GK = 'GK', 'Goalkeeper'
        DEF = 'DEF', 'Defender'
        MID = 'MID', 'Midfielder'
        FWD = 'FWD', 'Forward'

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, related_name='players')
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    position = models.CharField(max_length=10, choices=Position.choices)
    number = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name

    objects = models.Manager()
    filtered = PlayersFilterManager()


class Transfer(models.Model):
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='transfers')
    club_from = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, related_name='transfers_out')
    club_to = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, related_name='transfers_in')
    price = models.DecimalField(max_digits=15, decimal_places=2)
    tft_price = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.player} → {self.club_to} ({self.season})"

