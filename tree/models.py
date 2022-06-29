from time import timezone
from django.db import models
# Create your models here.


#These are all model objects which represent the tables in our database
class Neighborhood(models.Model):
    nid = models.AutoField(db_column='nId', primary_key=True)  # Field name made lowercase.
    neighborhood = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'neighborhood'

class Street(models.Model):
    sid = models.AutoField(db_column='sId', primary_key=True)  # Field name made lowercase.
    neighborhood = models.ForeignKey(Neighborhood, models.DO_NOTHING, db_column='neighborhood')
    address = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'street'
    

class Tree(models.Model):
    tid = models.AutoField(primary_key=True)
    type = models.ForeignKey('TreeType', models.DO_NOTHING, db_column='type')
    street = models.ForeignKey(Street, models.DO_NOTHING, db_column='street')
    alive = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tree'


class TreeType(models.Model):
    ttid = models.AutoField(primary_key=True)
    tree_type = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'tree_type'



class Calculation(models.Model):
    cid = models.AutoField(db_column='cId', primary_key=True)  # Field name made lowercase.
    tree = models.ForeignKey('Tree', models.DO_NOTHING, db_column='tree')
    description = models.CharField(db_column='Description', max_length=128, blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='YEAR')  # Field name made lowercase.
    biomass = models.DecimalField(db_column='Biomass', max_digits=9, decimal_places=2)  # Field name made lowercase.
    carbon_absorbed = models.DecimalField(db_column='Carbon_Absorbed', max_digits=9, decimal_places=4)  # Field name made lowercase.
    carbon_stocked = models.DecimalField(db_column='Carbon_Stocked', max_digits=9, decimal_places=4)  # Field name made lowercase.
    carbon_produced = models.DecimalField(db_column='Carbon_Produced', max_digits=9, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'calculation'


class RadiusData(models.Model):
    rdid = models.AutoField(db_column='rdId', primary_key=True)  # Field name made lowercase.
    tree = models.ForeignKey('Tree', models.DO_NOTHING, db_column='tree')
    radius = models.DecimalField(db_column='Radius', max_digits=7, decimal_places=2)  # Field name made lowercase.
    year = models.IntegerField(db_column='YEAR')  # Field name made lowercase.
    month = models.IntegerField(db_column='Month', blank=True, null=True)  # Field name made lowercase.
    biomass = models.DecimalField(db_column='Biomass', max_digits=9, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'radius_data'



class Result(models.Model):
    rid = models.AutoField(db_column='rId', primary_key=True)  # Field name made lowercase.
    tree = models.ForeignKey('Tree', models.DO_NOTHING, db_column='tree')
    tree_name = models.CharField(db_column='tree_Name', max_length=64)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=128)  # Field name made lowercase.
    year = models.IntegerField(db_column='YEAR')  # Field name made lowercase.
    carbon_absorbed = models.DecimalField(db_column='Carbon_Absorbed', max_digits=9, decimal_places=2)  # Field name made lowercase.
    carbon_stocked = models.DecimalField(db_column='Carbon_Stocked', max_digits=9, decimal_places=2)  # Field name made lowercase.
    carbon_produced = models.DecimalField(db_column='Carbon_Produced', max_digits=9, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'result'


