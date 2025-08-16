function updatePrice() {
  const people = parseInt(document.getElementById('people').value, 10) || 1;
  const costPerPerson = 50000; // You can make this dynamic from template if needed
  const totalCost = people * costPerPerson;
  document.getElementById('totalPrice').value = `${totalCost.toLocaleString()} MMK`;
}

function showReceipt(bookingId) {
  const name = document.getElementById('fullName').value.trim();
  const email = document.getElementById('email').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const people = parseInt(document.getElementById('people').value.trim(), 10);
  
  const totalCost = 50000 * people; // Same as updatePrice

  const date = document.getElementById('tourDate').innerText;
  const departureTimeElem = document.getElementById('tourDepartureTime');
  const departureTime = departureTimeElem ? departureTimeElem.innerText : "N/A";

  document.getElementById('rBookingId').innerText = bookingId;
  document.getElementById('rName').innerText = name;
  document.getElementById('rEmail').innerText = email;
  document.getElementById('rPhone').innerText = phone;
  document.getElementById('rPeople').innerText = people;
  document.getElementById('rDate').innerText = date;
  document.getElementById('rDepartureTime').innerText = departureTime;
  document.getElementById('rCost').innerText = `${totalCost.toLocaleString()} MMK`;

  document.getElementById('receiptOverlay').style.display = 'flex';
}

function closeReceipt() {
  document.getElementById('receiptOverlay').style.display = 'none';
  document.getElementById('bookingForm').reset();
  updatePrice();
}

// Attach event listener for form submission
document.getElementById('bookingForm').addEventListener('submit', function(e) {
  e.preventDefault(); // Prevent default form submission

  const name = document.getElementById('fullName').value.trim();
  const email = document.getElementById('email').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const people = parseInt(document.getElementById('people').value.trim(), 10);

  if (!name || !email || !phone || !people) {
    alert('Please fill out all fields!');
    return;
  }

  // Submit form via POST (classic way)
  e.target.submit();

  // Optionally, generate temporary booking ID for display
  const bookingId = 'BK' + Math.floor(Math.random() * 100000);
  showReceipt(bookingId);
});

window.onload = updatePrice;
