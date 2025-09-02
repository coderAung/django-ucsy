from django.utils import timezone
from datetime import datetime

class BookingListDTO:
    def __init__(
        self, id, booking_code, customer_name, package_title, status_display,
        created_date, created_time,
        status_updated_date, status_updated_time,
        available_tickets, total_capacity  # Add these parameters
    ):
        self.id = id
        self.booking_code = booking_code
        self.customer_name = customer_name
        self.package_title = package_title
        self.status_display = status_display
        self.created_date = created_date
        self.created_time = created_time
        self.status_updated_date = status_updated_date
        self.status_updated_time = status_updated_time
        self.available_tickets = available_tickets  # Available tickets
        self.total_capacity = total_capacity  # Total capacity
class BookingDetailDTO:
    def __init__(
        self, id, status, ticket_count, unit_price,
        customer_name, customer_email, customer_phone,
        package_title, package_departure, package_duration,
        created_date=None, created_time=None,
        status_updated_date=None, status_updated_time=None,
        available_tickets=None, total_capacity=None
    ):
        self.id = id
        self.status = status
        self.ticket_count = ticket_count
        self.unit_price = unit_price
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone
        self.package_title = package_title
        self.package_departure = package_departure
        self.package_duration = package_duration
        self.created_date = created_date
        self.created_time = created_time
        self.status_updated_date = status_updated_date
        self.status_updated_time = status_updated_time
        self.available_tickets = available_tickets
        self.total_capacity = total_capacity

    @property
    def total_price(self):
        return self.unit_price * self.ticket_count

class BookingFilterDTO:
    def __init__(self, status=None, query=None):
        self.status = status
        self.query = query