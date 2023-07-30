from django.shortcuts import render
import googlemaps
from django import forms

from django.shortcuts import render
import datetime

from memory_profiler import profile
from django.http import FileResponse, Http404
from django.conf import settings
import os
from app import magnitude
import time

GOOGLE_MAPS_API_KEY = 'AIzaSyAkE9DxAq49v0uUlHqMox0Z5mLwol5ckwA'


# @profile
class CityForm(forms.Form):
    city = forms.CharField(label='City', max_length=100)


# @profile
def get_lat_lng(city):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(city)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return {'lat': lat, 'lng': lng}


# @profile
def landing(request):
    return render(request, 'earthquake_magnitude/landing.html')


# @profile
def get_magnitude(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        lat_lng = {'lat': latitude, 'lng': longitude}
        return render(request, 'earthquake_magnitude/magnitude.html', {'lat_lng': lat_lng})
    return render(request, 'earthquake_magnitude/magnitude.html')


# @profile
def city_view(request):
    form = CityForm()
    city = None
    lat_lng = None
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            lat_lng = get_lat_lng(city)
    context = {
        'form': form,
        'city': city,
        'lat_lng': lat_lng
    }
    return render(request, 'earthquake_magnitude/index.html', context)


# @profile
def my_view(request):
    if request.method == 'POST':
        # Get the parameters from the form
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        datetime_string = request.POST.get('datetime')
        if datetime_string is not None:
            # Convert the date string to a datetime object
            datetime_obj = datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M')

            # Get the date and time strings from the datetime object
            date_string = datetime_obj.strftime('%m/%d/%Y')
            time_string = datetime_obj.strftime('%H:%M')

            # Call the Python function in the other file

            # start1 = time.time()
            result = magnitude.MLClassifier(date_string, time_string, latitude, longitude)
            magnitude_output, depth_output = result[0]
            # print("\nTime taken for ML preprocessing and Prediction Module to run: --- %.2f seconds --- " % (
            #             time.time() - start1))

            # Render the HTML template with the result
            return render(request, 'earthquake_magnitude/magnitude.html', {'magnitude_output': round(magnitude_output, 2),
                                                                           'depth_output': round(depth_output, 2)})
        else:

            return render(request, 'earthquake_magnitude/magnitude.html', {'error': 'Datetime field is required.'})

    else:
        # Set the initial value of the datetime field
        initial_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return render(request, 'earthquake_magnitude/magnitude.html', {'initial_datetime': initial_datetime})

# @profile
def video_player(request, video_id):
    video_files = {
        '1': 'blender_1.mp4',
        '2': 'blender_2.mp4',
        '3': 'blender_3.mp4',
        '4': 'blender_4_5.mp4',
        '5': 'blender_4_5.mp4',
        '6': 'blender_6.mp4',
        '7': 'blender_7.mp4',
        '8': 'blender_8.mp4',
    }

    video_file = video_files.get(video_id)
    if not video_file:
        raise Http404('Video not found')

    video_path = os.path.join(settings.MEDIA_ROOT, video_file)
    return FileResponse(open(video_path, 'rb'), content_type='video/mp4')