from django.db import models


def as_dict(o):
    return o.as_dict()

def array_as_dict(a):
    return list(map(lambda x: x.as_dict(), a))


class City(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def as_dict(self):
        return {
            'city_id': self.id,
            'name': self.name,
            'lines': array_as_dict(self.lines.all()),
            'transitions': array_as_dict(self.transitions)
        }

    @property
    def transitions(self):
        return Transition.objects.filter(from_station__line__city=self)


class Line(models.Model):
    city = models.ForeignKey(City, related_name='lines', null=False, blank=False)
    name = models.CharField(max_length=100)
    color = models.IntegerField()

    def __unicode__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'stations': array_as_dict(self.ordered_stations)
        }

    @property
    def ordered_stations(self):
        if self.stations.count() == 0:
            return []

        current = self.stations.get(prev_station__isnull=True)
        result = [current]
        while current.next_station is not None:
            current = current.next_station
            result.append(current)

        return result


class Station(models.Model):
    line = models.ForeignKey(Line, related_name='stations', null=False, blank=False)
    name = models.CharField(max_length=100)
    next_station = models.OneToOneField('self', related_name="prev_station", null=True, blank=True)
    prev_time = models.IntegerField(null=True, blank=True)
    next_time = models.IntegerField(null=True, blank=True)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    lt_coord = models.FloatField(default=0)
    ln_coord = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'coords': str(self.x_coord) + "," + str(self.y_coord),
            'next_station_id': self.next_station.id if self.next_station is not None else None,
            'next_time': self.next_time,
            'prev_time': self.prev_time,
            'lat': self.lt_coord,
            'lng': self.ln_coord
        }


class Transition(models.Model):
    from_station = models.ForeignKey(Station, related_name='transitions', null=False, blank=False)
    to_station = models.ForeignKey(Station, null=False, blank=False)
    time = models.IntegerField()

    def __unicode__(self):
        return self.from_station.__unicode__() + '/' + self.to_station.__unicode__()

    def as_dict(self):
        return {
            'from_id': self.from_station.id,
            'to_id': self.to_station.id,
            'time': self.time
        }