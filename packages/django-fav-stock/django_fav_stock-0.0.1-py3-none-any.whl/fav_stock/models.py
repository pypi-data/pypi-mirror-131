from django.db import models


class ModelFavStock(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=30, null=True)
    remarks = models.CharField('Remarks', max_length=500, blank=True, null=True)
    red = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    modified_time = models.DateTimeField(auto_now=True)

    # for fix pycharm warning
    # https://stackoverflow.com/questions/43865989/unresolved-attribute-reference-objects-for-class-in-pycharm
    objects = models.Manager()

    def __str__(self):
        return str(self.code) + ' / ' + str(self.name) + ' / ' + str(self.remarks)
