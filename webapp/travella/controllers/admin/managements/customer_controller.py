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


def detail(request:HttpRequest, id:uuid) -> HttpResponse:
    return render(request, view('customer-detail'))
