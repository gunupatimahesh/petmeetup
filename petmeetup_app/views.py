import json

from django.contrib import messages
from django.http import QueryDict, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import QueryDict, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from petmeetup_app.forms import PetMeetUpForm
from petmeetup_app.models import PetMeetUp, PetType, PetBreed
from petmeetup_app.serializers import PetMeetUpSerializer


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Change 'home' to the name of your home view
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')  # Change 'login' to the name of your login view


@api_view(['GET', 'POST'])
def pet_meetup_list(request):
    # Use QueryDict for query parameters
    if request.method == 'GET':
        params = QueryDict(request.GET.urlencode())

        # Extract parameters from the query parameters
        pet_type = params.get('pet_type', None)
        pet_breed = params.get('pet_breed', None)
        age_min = params.get('age_min', None)
        age_max = params.get('age_max', None)
        available_for_meet_up = params.get('available_for_meet_up', None)
        need_day_care = params.get('need_day_care', None)

        # Build a queryset based on the parameters
        queryset = PetMeetUp.objects.all()

        if pet_type:
            queryset = queryset.filter(pet_type__name=pet_type)

        if pet_breed:
            queryset = queryset.filter(pet_breed__name=pet_breed)

        if age_min:
            queryset = queryset.filter(age__gte=age_min)

        if age_max:
            queryset = queryset.filter(age__lte=age_max)

        if available_for_meet_up is not None:
            # Handle boolean parameter using QueryDict
            available_for_meet = params.get('available_for_meet', '').lower() == 'true'
            queryset = queryset.filter(available_for_meet_up=available_for_meet_up)
        if need_day_care is not None:
            # Handle boolean parameter using QueryDict
            need_day_care = params.get('need_day_care', '').lower() == 'true'
            queryset = queryset.filter(need_day_care=need_day_care)
        serializer = PetMeetUpSerializer(queryset, many=True)
        return Response(serializer.data)
        # Add more filters as needed based on other parameters
    if request.method == 'POST':
        # Deserialize the data using the updated serializer
        serializer = PetMeetUpSerializer(data=request.data)

        if serializer.is_valid():
            # Convert pet_type and pet_breed names to instances
            pet_type_name = serializer.validated_data.get('pet_type')
            pet_breed_name = serializer.validated_data.get('pet_breed')

            try:
                # Try to get PetType and PetBreed instances in a case-insensitive way
                pet_type_instance = PetType.objects.get(name__iexact=pet_type_name)
                pet_breed_instance = PetBreed.objects.get(name__iexact=pet_breed_name)

                # Update the serializer data with instances
                serializer.validated_data['pet_type'] = pet_type_instance
                serializer.validated_data['pet_breed'] = pet_breed_instance

                # Save the serializer with updated data
                serializer.save()

                return Response(serializer.data, 201)

            except PetType.DoesNotExist:
                return Response({"pet_type": ["PetType matching query does not exist."]}, status=400)

            except PetBreed.DoesNotExist:
                return Response({"pet_breed": ["PetBreed matching query does not exist."]}, status=400)

        return Response(serializer.errors, status=400)


def dashboard_view(request):
    return render(request, 'dashboard.html')


def pet_meetup_list_view(request):
    if request.method == 'GET':
        params = QueryDict(request.GET.urlencode())

        pet_type = params.get('pet_type', None)
        pet_breed = params.get('pet_breed', None)
        age_min = params.get('age_min', None)
        age_max = params.get('age_max', None)
        available_for_meet_up = params.get('available_for_meet_up', None)
        need_meetup = params.get('need_meetup', None)
        need_day_care = params.get('need_day_care', None)

        queryset = PetMeetUp.objects.all()

        if pet_type:
            queryset = queryset.filter(pet_type__name=pet_type)

        if pet_breed:
            queryset = queryset.filter(pet_breed__name=pet_breed)

        if age_min:
            queryset = queryset.filter(age__gte=age_min)

        if age_max:
            queryset = queryset.filter(age__lte=age_max)

        available_meetups = []
        need_meetups = []
        day_care_meetups = []

        for meetup in queryset:
            if available_for_meet_up is not None and meetup.available_for_meet_up == (
                    available_for_meet_up.lower() == 'true'):
                available_meetups.append(meetup)
            elif need_meetup is not None and meetup.need_meetup == (need_meetup.lower() == 'true'):
                need_meetups.append(meetup)
            elif need_day_care is not None and meetup.need_day_care == (need_day_care.lower() == 'true'):
                day_care_meetups.append(meetup)

        return render(request, 'pet_meetup_list.html', {
            'available_meetups': available_meetups,
            'need_meetups': need_meetups,
            'day_care_meetups': day_care_meetups,
        })

    # Handle other HTTP methods as needed
    else:
        # Return an error response for unsupported methods
        return HttpResponse(status=405)


def pet_details(request, pet_id):
    try:
        pet = PetMeetUp.objects.get(pk=pet_id)
        return render(request, 'pet_details.html', {'pet': pet})
    except PetMeetUp.DoesNotExist:
        # Handle the case where the pet with the given ID doesn't exist
        return render(request, 'pet_not_found.html')


def api_post_handler(request):
    if request.method == 'POST':
        form = PetMeetUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to a success page
    else:
        form = PetMeetUpForm()

    return render(request, 'register_pet.html', {'form': form})
