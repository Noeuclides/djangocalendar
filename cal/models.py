from django.db import models
from django.core.exceptions import ValidationError


class Grade(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)

    def clean(self):
        challenge = Challenge.objects.filter(
            grade=self.grade,
        )
        if not challenge:
            raise ValidationError(
                'No hay Retos con este espacio de cocreación.')

        workteams = WorkTeam.objects.all().select_related('challenge')
        workteam_list = [workteam.challenge for workteam in workteams]
        if not any(workteam in challenge for workteam in list(set(workteam_list))):
            raise ValidationError(
                'No hay equipos de trabajo con los retos que tienen ese espacio de cocreación, por lo tanto no hay ningún equipo de trabajo que realice el evento.')

    def __str__(self):
        return self.title


class Activity(models.Model):
    name = models.CharField(max_length=500)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Activity, self).save(*args, **kwargs)
        try:
            challenge = Challenge.objects.filter(
                grade=self.event.grade,
            )

            workteams = WorkTeam.objects.all().select_related('challenge')

            for workteam in workteams:
                if workteam.challenge in challenge:
                    activities = workteam_activity(
                        workteam=workteam, activity=self)
                    print(activities)
                    activities.save()

        except Exception as e:
            print(e)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    name = models.CharField(max_length=500)
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class WorkTeam(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def __str__(self):
        return self.challenge


class workteam_activity(models.Model):
    workteam = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    class Meta:
        unique_together = ('workteam', 'activity',)

