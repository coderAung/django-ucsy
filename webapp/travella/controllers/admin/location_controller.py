from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from travella.domains.models.tour_models import Location
from travella.domains.forms.location_forms import LocationForm

def _get_all_locations_with_counts():
    return Location.objects.annotate(package_count=Count('packages')).order_by('name')

@login_required
def location_list(request):
    query = request.GET.get('q', '')
    locations = _get_all_locations_with_counts()
    if query:
        locations = locations.filter(name__icontains=query)
    context = {
        'locations': locations,
        'total_locations': locations.count(),
        'query': query,
        'form': LocationForm()
    }
    return render(request, 'admin/locations/list.html', context)

@login_required
def location_add(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.created_by = request.user
            location.save()
            messages.success(request, 'Location added successfully.')
            return redirect('location_list')
        else:

            locations = _get_all_locations_with_counts()
            context = {
                'locations': locations,
                'total_locations': locations.count(),
                'form': form,
                'show_add_modal': True
            }
            messages.error(request, 'Please correct the error below.')
            return render(request, 'admin/locations/list.html', context)
    return redirect('location_list')

@login_required
def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location updated successfully.')
            return redirect('location_list')
        else:
            locations = _get_all_locations_with_counts()
            context = {
                'locations': locations,
                'total_locations': locations.count(),
                'edit_form': form,
                'edit_location_pk': pk,
                'show_edit_modal': True
            }
            messages.error(request, 'Please correct the error below.')
            return render(request, 'admin/locations/list.html', context)
    return redirect('location_list')

@login_required
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if location.packages.count() > 0:
        messages.error(request, f'Cannot delete "{location.name}" because it is linked to existing packages.')
        return redirect('location_list')
    if request.method == 'POST':
        location.delete()
        messages.success(request, 'Location deleted successfully.')
    return redirect('location_list')