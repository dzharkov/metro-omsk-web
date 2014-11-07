from django.db import models
from django.db.models import SET_NULL
from django.db.models.signals import post_save

def as_dict(o):
    return o.as_dict()


def array_as_dict(a):
    return list(map(lambda x: x.as_dict(), a))


MAX_ABS_COORDS = 400

class City(models.Model):
    name = models.CharField(max_length=100)
    lt_coord = models.FloatField(default=0)
    ln_coord = models.FloatField(default=0)
    top_coord = models.FloatField(default=MAX_ABS_COORDS)
    bottom_coord = models.FloatField(default=-MAX_ABS_COORDS)
    left_coord = models.FloatField(default=MAX_ABS_COORDS)
    right_coord = models.FloatField(default=-MAX_ABS_COORDS)

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
    color = models.CharField(max_length=10, default='#FF0000')

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
    next_station = models.OneToOneField('self', related_name="prev_station", null=True, blank=True, on_delete=SET_NULL)
    prev_time = models.IntegerField(null=True, blank=True)
    next_time = models.IntegerField(null=True, blank=True)
    lt_coord = models.FloatField(default=0)
    ln_coord = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x_coord,
            'y': self.y_coord,
            'next_station_id': self.next_station.id if self.next_station is not None else None,
            'next_time': self.next_time,
            'prev_time': self.prev_time,
            'lat': self.lt_coord,
            'lng': self.ln_coord
        }

    def update_bounding_rect(self, city):
        city.top_coord = min(city.top_coord, float(self.lt_coord))
        city.bottom_coord = max(city.bottom_coord, float(self.lt_coord))
        city.left_coord = min(city.left_coord, float(self.ln_coord))
        city.right_coord = max(city.right_coord, float(self.ln_coord))

    def update_city_bounding_rect(self):
        city = self.line.city
        self.update_bounding_rect(city)
        city.save()

    @property
    def x_coord(self):
        city = self.line.city
        delta_x = city.right_coord - city.left_coord
        if delta_x == 0:
            return 0
        return (self.ln_coord - city.left_coord) / delta_x

    @property
    def y_coord(self):
        city = self.line.city
        delta_y = city.bottom_coord - city.top_coord
        if delta_y == 0:
            return 0
        return (self.lt_coord - city.top_coord) / delta_y


def update_br(sender, instance, *args, **kwards):
    if sender == Station:
        #pass
        instance.update_city_bounding_rect()

post_save.connect(update_br)

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
