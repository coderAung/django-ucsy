import uuid

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from travella.services import customer_service

base = 'admin/managements/users/'

def view(name:str) -> str:
    return base + name + '.html'

# customers/ GET
def list(request):

    search_query = request.GET.get('search_query', '').strip()

    if search_query:
        customers_qs = customer_service.get_filtered_customers(query=search_query)
    else:
        customers_qs = customer_service.get_all_customers()

    context = {
        'customers': customers_qs,
        'search_query': search_query,

    }


    return render(request, view('customer-list'), context)


def detail(request: HttpRequest, id: uuid.UUID) -> HttpResponse:  # Changed 'account_id' to 'id'
    """
    Displays the details for a specific customer.
    """
    try:
        # Get the specific customer from the service using the 'id' from the URL
        customer = customer_service.get_customer_detail(account_id=id)  # Pass 'id' to the service

        # Get the booking history for that customer from the service
        customer_bookings = customer_service.get_bookings_for_customer(customer_account=customer)

    except customer_service.Account.DoesNotExist:
        return render(request, 'admin/error.html', {'message': 'Customer not found.'})

    context = {
        'customer': customer,
        'customer_bookings': customer_bookings
    }
    return render(request, view('customer-detail'), context)