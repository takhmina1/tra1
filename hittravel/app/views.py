from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Tour, TourRequest
from .serializers import TourSerializer, TourRequestSerializer

class TourListCreateView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city', None)
        filters = {'city': city}
        tours = Tour.objects.filter(**filters)
        serializer = self.get_serializer(tours, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            tour = serializer.save()
            self.send_notification(tour)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_notification(self, tour):
        message = f"Новый тур добавлен: {tour.city} - {tour.date}"
        # Ваш код отправки уведомления (например, через почту, пуш-уведомления и т.д.)

class TourRequestListCreateView(generics.ListCreateAPIView):
    queryset = TourRequest.objects.all()
    serializer_class = TourRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        filters = {}  # Ваши фильтры для запроса
        tour_requests = TourRequest.objects.filter(**filters)
        serializer = self.get_serializer(tour_requests, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            tour_request = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TourRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourRequest.objects.all()
    serializer_class = TourRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
