from django.http import HttpResponse
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from reservation_app.models import MainHall, Reservation

# Create your views here.
def add_room(request):
    rooms = MainHall.objects.all()
    errors = []
    if request.method == 'GET':
        return render(request, 'add_room.html')

    elif request.method == 'POST':
        name = request.POST.get('name')
        room_capacity = request.POST.get('room_capacity')
        projector = request.POST.get('projector')

        if name is not None:
            for room in rooms:
                if name == room.name:
                    errors.append('Wprowadzona nazwa sali już istnieje w bazie. Wprowadź jeszcze raz!')

        if name is None or name == "":
        # if not name:
            errors.append('Wprowadź nazwę sali')

        if not room_capacity.isdigit():
            errors.append('Room capacity must be integer value!')
        if int(room_capacity) <= 0:
            errors.append('Room capacity must be positive value!')

        projector = projector == 'on'

        if len(errors) == 0:
            MainHall.objects.create(name=name, room_capacity=room_capacity, projector=projector)

            return HttpResponse (f'Sala o nazwie {name} została dodana!')
    return render(request, 'add_room.html', context={'rooms': rooms, 'errors': errors})


def rooms_list(request):
    rooms = MainHall.objects.all().order_by('room_capacity')
    reservations = Reservation.objects.all()
    current_date = date.today()
    for room in rooms:
        reservation_dates = []
        room_reservations = room.reservation_set.all()
        for room_reservation in room_reservations:
            reservation_dates.append(room_reservation.date)
            # if current_date in reservation_dates:
            #     room.reserved = 'no' #dlaczego tutaj nie może być nazwa z podkreślnikiem, tylko musi być kropka???
            # elif current_date not in reservation_dates:
            #     room.reserved = 'yes'

    # for room in rooms:
    #     reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
    #
        room.reserved = date.today() in reservation_dates

    return render(request, 'rooms_list.html', context={'rooms': rooms, 'reservations': reservations,
                                                       'current_date': current_date,
                                                       'reservation_dates': reservation_dates})


def room_details(request, room_id):

    if request.method == 'GET':
        room = MainHall.objects.get(id=room_id)
        reservations = room.reservation_set.all().order_by('-date')
        current_date = date.today()
        reservation_dates = []
        for reservation in reservations:
            reservation_dates.append(reservation.date)
        room.reserved = current_date in reservation_dates
        # if current_date == reservations.date:
        #     room_availability = 'yes'
        # elif current_date == reservations.date:
        #     room_availability = 'no'

        return render(request, 'room_details.html', context={'room': room, 'reservations': reservations,
                                                             'current_date': current_date})


def modify_room(request, room_id):
    rooms = MainHall.objects.all()
    errors = []
    if request.method == 'GET':
        room = MainHall.objects.get(id=room_id)
        return render(request, 'modify_room.html', context={'room': room})

    elif request.method == 'POST':
        room = MainHall.objects.get(id=room_id)
        name = request.POST.get('name')
        room_capacity = request.POST.get('room_capacity')
        projector = request.POST.get('projector')
        # if name is None and name != "":
        if not name:
            errors.append('Wprowadź nazwę sali')
        if name is not None:
            for room in rooms:
                if name == room.name:
                    errors.append('Wprowadzona sala już istnieje. Podaj inną nazwę!')
        if int(room_capacity) <= 0:
            errors.append('Wprowadź prawidłową pojemność danej sali')

        projector = projector == 'on'

        if len(errors) == 0:
            room.name = name
            room.room_capacity = room_capacity
            room.projector = projector
            room.save()
            return redirect(f'/rooms', context={'rooms': rooms, 'errors': errors})
        return render(request, 'modify_room.html', context={'rooms': rooms, 'errors': errors})

        # return render(request, 'rooms_list.html', context={'rooms': rooms, 'errors': errors})
        # elif len(errors) != 0:
        #     return render(request, 'modify_room.html', context={'rooms': rooms, 'errors': errors})


def delete_room(request, room_id):
    rooms = MainHall.objects.all()
    if request.method == 'GET':
        room = MainHall.objects.get(id=room_id)
        room.delete()
        return render(request, 'rooms_list.html', context={'room': room, 'rooms': rooms})

def room_reservation(request, room_id):
    rooms = MainHall.objects.all()
    errors = []
    if request.method == 'GET':
        room = MainHall.objects.get(id=room_id)
        return render(request, 'room_reservation.html', context={'room': room, 'rooms': rooms})

    elif request.method == 'POST':
        room = MainHall.objects.get(id=room_id)
        date = request.POST.get('reservation_date')
        comment = request.POST.get('comment')
        if Reservation.objects.filter(room=room, date=date):
            errors.append('Sala jest już zarezerwowana!')
            return render(request, 'room_reservation.html', context={'room': room, 'errors': errors})
        if date < str(datetime.date.today()):
            errors.append('Data jest z przeszłości!')
            return render(request, 'room_reservation.html', context={'room': room, 'errors': errors})

        Reservation.objects.create(room=room, date=date, comment=comment)
        # return HttpResponse('Sala została zarezerwowana w wybranym terminie!')
        return redirect('/rooms')

# class RoomReserveView(View):
#     def get(self, request, room_id):
#         room = get_object_or_404(Room, id=room_id)
#         if room.projector:
#             room.projector = 'Yes'
#         else:
#             room.projector = 'No'
#         room_reservations = room.reservation_set.all().order_by('-date')
#         for room_reservation in room_reservations:
#             room_reservation.date = date.strftime(room_reservation.date, '%Y-%m-%d')
#         return render(request, 'reserve_room.html',
#                       context={'room': room,
#                                'room_reservations': room_reservations})
#
#     def post(self, request, room_id):
#         reservation_date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
#         comment = request.POST.get('comment')
#         confirmation = request.POST.get('confirm')
#         room = get_object_or_404(Room, id=room_id)
#         today_date = date.today()
#         if confirmation:
#             errors = []
#             if reservation_date:
#                 if reservation_date < today_date:
#                     errors.append('Selected date relates to the past')
#                 else:
#                     reservation_date = date.strftime(reservation_date, '%Y-%m-%d')
#             else:
#                 errors.append('Reservation date has to be selected')
#             room_reservations = room.reservation_set.all()
#             for room_reservation in room_reservations:
#                 if date.strftime(room_reservation.date, '%Y-%m-%d') == reservation_date:
#                     errors.append('Room is already booked at that date')
#             if len(errors) == 0:
#                 Reservation.objects.create(date=reservation_date, comment=comment, room_id=room)
#                 return redirect('/room/list')
#             else:
#                 room_reservations = room.reservation_set.all().order_by('-date')
#                 for room_reservation in room_reservations:
#                     room_reservation.date = date.strftime(room_reservation.date, '%Y-%m-%d')
#                 return render(request, 'reserve_room.html',
#                               context={'room': room,
#                                        'errors': errors,
#                                        'room_reservations': room_reservations})