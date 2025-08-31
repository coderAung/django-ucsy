// C:\BookTour\webapp\travella\static\js\customer.js

// Function to display a custom alert modal with a title and message
function showAlertModal(title, message) {
    const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
    document.getElementById('alertTitle').textContent = title;
    document.getElementById('alertMessage').textContent = message;
    alertModal.show();
}

// This function updates the total price and handles client-side validation
// for the number of people.
function updatePrice() {
    const peopleInput = document.getElementById('people');
    let people = parseInt(peopleInput.value) || 1;
    const price = parseFloat(document.getElementById('pricePerSeat').value) || 0;
    
    // Get available seats from the DOM for validation
    const availableSeatsElement = document.getElementById('availableSeatsValue');
    const maxSeats = parseInt(availableSeatsElement.textContent) || 0;

    // Client-side validation: prevent choosing more than available seats
    if (maxSeats > 0 && people > maxSeats) {
        people = maxSeats;
        peopleInput.value = people; // Update the input field to reflect the max limit
        showAlertModal("Booking Error", `Sorry, there are only ${maxSeats} seats available.`);
    }

    // Client-side validation: ensure at least 1 person is selected
    if (people < 1) {
        people = 1;
        peopleInput.value = people;
    }

    // Calculate the total cost and format it as currency
    const total = (people * price).toFixed(2);
    
     const formattedNumber = new Intl.NumberFormat('en-US', {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(total);

    // Manually add the currency code after the number
    document.getElementById('totalPrice').value = `${formattedNumber} MMK`;
        
}

// This code runs when the entire page content is loaded
document.addEventListener('DOMContentLoaded', function() {
    // --- Initial Setup ---
    const peopleInput = document.getElementById('people');
    const receiptModal = new bootstrap.Modal(document.getElementById('receiptConfirmationModal'));
    const availableSeats = parseInt(document.getElementById('availableSeatsValue').textContent);

    // Initialize price calculation on page load
    updatePrice();
    
    // Add event listeners for the number of people input field
    peopleInput.addEventListener('input', updatePrice);
    peopleInput.addEventListener('change', updatePrice);
    
    // --- Button Handlers for Increment/Decrement ---
    document.getElementById('increasePeople').addEventListener('click', () => {
        let currentVal = parseInt(peopleInput.value);
        if (isNaN(currentVal)) currentVal = 1;

        if (currentVal < availableSeats) {
            peopleInput.value = currentVal + 1;
            updatePrice();
        } else {
            showAlertModal("Booking Error", `Sorry, there are only ${availableSeats} seats available.`);
        }
    });

    document.getElementById('decreasePeople').addEventListener('click', () => {
        let currentVal = parseInt(peopleInput.value);
        if (isNaN(currentVal)) currentVal = 1;
        
        if (currentVal > 1) {
            peopleInput.value = currentVal - 1;
            updatePrice();
        }
    });

    // --- Show Receipt Button Click Handler (Client-Side Validation & Modal Population) ---
    document.getElementById('showReceiptBtn').addEventListener('click', function() {
        // Validate the form for required fields (uses Bootstrap's validation)
        const form = document.getElementById('bookingForm');
        form.classList.add('was-validated');
        
        if (!form.checkValidity()) {
            return;
        }

        // Gather data from the form to display in the modal
        const formData = {
            name: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            people: parseInt(document.getElementById('people').value) || 1,
            packageTitle: document.getElementById('tourPackageTitle').textContent,
            departureDate: document.getElementById('tourDate').innerText,  
             endDate: document.getElementById('tourEndDate').innerText,
            pricePerSeat: parseFloat(document.getElementById('pricePerSeat').value) || 0
        };
        
        // Calculate the final total cost
        const totalCost = (formData.people * formData.pricePerSeat).toFixed(2);
        
        // Populate the modal with the gathered temporary data
      // document.getElementById('receiptBookingId').textContent = 'TMP-' + Date.now();
        document.getElementById('receiptDate').textContent = new Date().toLocaleDateString();
        document.getElementById('receiptName').textContent = formData.name;
        document.getElementById('receiptEmail').textContent = formData.email;
        document.getElementById('receiptPhone').textContent = formData.phone;
        document.getElementById('receiptPackage').textContent = formData.packageTitle;
        document.getElementById('receiptDeparture').textContent = formData.departureDate;
         document.getElementById('receiptEndDate').textContent = formData.endDate;
        document.getElementById('receiptTravelers').textContent = formData.people;
      // Apply currency formatting to the receipt total in the modal
        const formattedReceiptTotal = new Intl.NumberFormat('en-US', { 
            style: 'decimal', 
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }).format(totalCost);
        document.getElementById('receiptTotal').textContent = `${formattedReceiptTotal} MMK`;
        
        
        // Show the confirmation modal to the user
        receiptModal.show();
    });
    
    // --- Final Confirmation Handler (Server-Side Booking Creation) ---
    document.getElementById('confirmSaveBtn').addEventListener('click', function() {
        const form = document.getElementById('bookingForm');
        const formData = new FormData(form);
        
        // Send a POST request to the server to create the booking
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showAlertModal("Booking Failed", data.error);
                throw new Error(data.error);
            }
            
            // On success, update the modal with real data from the server response
           /* if (data.booking_id) {
                document.getElementById('receiptBookingId').textContent = data.booking_id;
            }*/
            if (data.booking_date) {
                const bookingDate = new Date(data.booking_date);
                document.getElementById('receiptDate').textContent = bookingDate.toLocaleDateString();
            }
            
            // Hide the modal immediately
            receiptModal.hide();
            
            // Redirect to the booking detail page instead of showing alert
            window.location.href = `/customer/bookings/${data.booking_id}/`;
            
        })
        .catch(error => {
            console.error('Error:', error);
            showAlertModal("Booking Failed", "An unexpected error occurred. Please try again.");
        });
    });
});