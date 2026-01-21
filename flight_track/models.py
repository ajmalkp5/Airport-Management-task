from django.db import models

class AirportRoute(models.Model):
    """
    Model to store airport routes with their positions and duration.

    Fields:
        airport_code (CharField): The IATA/airport code (max 10 characters).
        position (CharField): Position/direction, either 'L' (Left) or 'R' (Right).
        duration (IntegerField): Duration of the route in minutes.
    """
    airport_code = models.CharField(max_length=10)
    position = models.CharField(
        max_length=1,
        choices=[('L', 'Left'), ('R', 'Right')]
    )
    duration = models.IntegerField()

    class Meta:
        # Ensure the combination of airport_code + position is unique
        unique_together = ('airport_code', 'position')
        verbose_name = "Airport Route"
        verbose_name_plural = "Airport Routes"

    def __str__(self):
        return f"{self.airport_code} - {self.position} - {self.duration}"
