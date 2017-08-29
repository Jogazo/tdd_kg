from django.db import models


class MediaAppearance(models.Model):
    dag = models.DateField('Datum van publicatie / media optreden.')
    tijd = models.TimeField('Tijdstip.', null=True, blank=True)
    omschrijving = models.TextField('Korte omschrijving.', default='')

    def __str__(self):
        return '{} {} {}'.format(self.dag, self.tijd, self.omschrijving)
