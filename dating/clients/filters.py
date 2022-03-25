import django_filters
from geopy import distance

from .models import Client


class ClientFilter(django_filters.FilterSet):
    """
    Custom filter class for ClientListViewSet.

    Accepted query parameters:
    -'gender' - string, accept two options: 'мужской' or 'женский';
    -'first_name' - string, show clients with entered first names;
    -'last_name' - string, show clients with entered last names;
    -'distance' - float or ineger, show clients within entered distance.
    """
    distance = django_filters.NumberFilter(method='check_distance')

    def check_distance(self, queryset, name, value):
        """Approximately filter clients according to distance
        from current user.

        Inaccuracy get longer distances for directions that
        differ from accurately east, west, north and south.
        The reason is that the function limits the region not by circle,
        but by square.
        """
        current_user = self.request.user
        point1_coords = (current_user.latitude, current_user.longitude)
        long1 = distance.distance(kilometers=float(value)).destination(
            point1_coords, bearing=270
        ).longitude
        long2 = distance.distance(kilometers=float(value)).destination(
            point1_coords, bearing=90
        ).longitude
        lat1 = distance.distance(kilometers=float(value)).destination(
            point1_coords, bearing=180
        ).latitude
        lat2 = distance.distance(kilometers=float(value)).destination(
            point1_coords, bearing=0
        ).latitude
        return queryset.filter(
            longitude__range=(long1, long2)).filter(
                latitude__range=(lat1, lat2)
            )

    class Meta:
        model = Client
        fields = ['gender', 'first_name', 'last_name']
