from django.db import models
import uuid


class Scan(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, blank=True)
    location = models.URLField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.uuid)


class Device(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.GenericIPAddressField(unique=True)
    device_type = models.CharField(default='autodetect', max_length=255, blank=True)
    hostname = models.CharField(max_length=255, blank=True)
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True)
    os_version = models.CharField(max_length=255, blank=True)
    uptime = models.CharField(max_length=255, blank=True)
    serial = models.CharField(max_length=255, blank=True)
    mac = models.CharField(max_length=255, blank=True)
    hardware = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.ip)


class Interface(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    mac = models.CharField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    device = models.OneToOneField(Device, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ip)


class Host(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    mac = models.CharField(max_length=255, unique=True, blank=True)
    vlan = models.CharField(max_length=255, blank=True)
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    access_interface = models.ManyToManyField(Interface)
    scans_found = models.ManyToManyField(Scan)

    def __str__(self):
        return str(self.ip)
