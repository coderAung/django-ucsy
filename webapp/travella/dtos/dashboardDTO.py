from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DashboardDTO:
  total_bookings: int
  total_packages: int
  new_customers: int
  active_customers: int
  top_packages: List[Dict[str,int]]
  pending_bookings: int
  cancel_bookings: int
  pending_payment: float
  total_feedbacks: int
  monthly_bookings_data: Dict[str, List]