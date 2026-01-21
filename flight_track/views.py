from django.shortcuts import render
from .models import AirportRoute
from .forms import NthNodeForm
from django.http import JsonResponse



def nth_route(request):
    """
    Handle Nth left or right node request.

    GET: Render a form to select airport, position, and N.
    POST: Validate form and return the Nth route for the given airport and position.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with form and result.
    """
    form = NthNodeForm()
    result = None

    if request.method == "POST":
        form = NthNodeForm(request.POST)
        if form.is_valid():
            airport = form.cleaned_data['airport_code']
            position = form.cleaned_data['position']
            n = form.cleaned_data['n']

            routes = AirportRoute.objects.filter(
                airport_code=airport,
                position=position
            ).order_by('id')

            if routes.count() >= n:
                result = routes[n-1]
            else:
                result = "No such route"

    return render(request, "flight_track/nth_node.html", {
        "form": form,
        "result": result
    })



def longest_route(request):
    """
    Display the route with the longest duration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with the longest route.
    """
    route = AirportRoute.objects.order_by('-duration').first()
    return render(request, "flight_track/longest.html", {"route": route})



def shortest_route(request):
    """
    Display the shortest route between two airports.

    POST: Accept 'start' and 'end' airport codes and return the route with the shortest duration
          among matching records.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with the shortest route result.
    """
    result = None

    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")
        result = AirportRoute.objects.filter(
            airport_code__in=[start, end]
        ).order_by('duration').first()

    return render(request, "flight_track/shortest.html", {"result": result})



def dashboard(request):
    """
    Render the main dashboard page for the flight tracking application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page for the dashboard.
    """
    return render(request, "flight_track/dashboard.html")



def get_routes(request):
    """
    Return all airport routes as a JSON response.

    GET: Returns all routes with their ID, airport code, position, and duration.
    Other methods: Return a 405 error.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing all routes or an error message.
    """
    if request.method == "GET":
        routes = AirportRoute.objects.all()

        data = []
        for route in routes:
            data.append({
                "id": route.id,
                "airport_code": route.airport_code,
                "position": route.position,
                "duration": route.duration
            })

        return JsonResponse({
            "status": "success",
            "count": len(data),
            "routes": data
        })

    return JsonResponse({
        "status": "error",
        "message": "Only GET method allowed"
    }, status=405)



def route_list(request):
    """
    Render a page displaying a list of all airport routes.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with all routes.
    """
    routes = AirportRoute.objects.all()
    return render(request, "flight_track/route_list.html", {
        "routes": routes
    })



def create_route(request):
    """
    Handle creation of a new airport route.

    GET: Render the form to create a route.
    POST: Save the submitted route data and display a success message on the same page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML form page with optional success message.
    """
    success = None  # Flag for template

    if request.method == "POST":
        airport_code = request.POST.get("airport_code")
        position = request.POST.get("position")
        duration = request.POST.get("duration")

        if airport_code and position and duration:
            AirportRoute.objects.create(
                airport_code=airport_code,
                position=position,
                duration=duration
            )
            success = "Route saved successfully!"  

    return render(request, "flight_track/create_route.html", {"success": success})
