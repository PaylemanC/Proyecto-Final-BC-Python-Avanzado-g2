from django.db import models


class Bills(models.Model):
    bill_id = models.TextField(primary_key=True)
    number = models.IntegerField()
    type = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bills'


class Congress(models.Model):
    congress_id = models.TextField(primary_key=True)
    session = models.TextField()
    number = models.IntegerField()
    start_date = models.TextField(blank=True, null=True)
    end_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'congress'


class Members(models.Model):
    member_id = models.TextField(primary_key=True)
    name = models.TextField()
    party_code = models.ForeignKey('Parties', db_column='party_code', on_delete=models.CASCADE)
    state_code = models.ForeignKey('States', db_column='state_code', on_delete=models.CASCADE)
    image_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'members'


class Parties(models.Model):
    party_code = models.TextField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'parties'


class RollCalls(models.Model):
    roll_call_id = models.TextField(primary_key=True)
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    congress = models.ForeignKey(Congress, on_delete=models.CASCADE)
    status = models.TextField(blank=True, null=True)
    date = models.TextField()
    loaded_etl_at = models.TextField()

    class Meta:
        managed = False
        db_table = 'roll_calls'


class States(models.Model):
    state_code = models.TextField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'states'


class Votes(models.Model):
    vote_id = models.TextField(primary_key=True)
    roll_call = models.ForeignKey(RollCalls, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    vote = models.TextField()

    class Meta:
        managed = False
        db_table = 'votes'
