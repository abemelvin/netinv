from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone

from .models import Device, Scan, Host
from .forms import ScanForm
from .tasks import execute_scan

from threading import Thread


def index(request):
    scan_list = Scan.objects.order_by('-start_date')[:10]
    context = {
        'title': 'Scans',
        'scan_list': scan_list,
    }
    return render(request, 'scans/index.html', context)

def detail(request, scan_id):
    scan = get_object_or_404(Scan, pk=scan_id)
    return render(request, 'scans/detail.html', {'scan': scan})

def new(request):
    if request.method == "POST":
        form = ScanForm(request.POST)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.author = request.user
            scan.start_date = timezone.now()
            scan.status = 'Queued'
            scan.save()
            t = Thread(target=execute_scan, args=[scan.pk])
            t.setDaemon(True)
            t.start()
            return redirect('scans:index')
    else:
        form = ScanForm()
    return render(request, 'scans/new.html', {'form': form, 'title': 'New Scan'})

def devices(request):
    device_list = Device.objects.order_by('pk')
    context = {
        'title': 'Devices',
        'device_list': device_list,
    }
    return render(request, 'scans/devices.html', context)