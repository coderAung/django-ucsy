# travella/dtos/booking_dto.py

class BookingListDTO:
    def __init__(self, id, customer_name, package_title, booked_date, status_display, time):
        self.id = id
        self.customer_name = customer_name
        self.package_title = package_title
        self.booked_date = booked_date
        self.status_display = status_display
        self.time = time


class BookingDetailDTO:
    def __init__(
        self, id, status, ticket_count, unit_price,
        customer_name, customer_email, customer_phone,
        package_title, package_departure, package_duration
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

    @property
    def total_price(self):
        return self.unit_price * self.ticket_count

class BookingFilterDTO:
    def __init__(self, status=None, query=None):
        self.status = status
        self.query = query
