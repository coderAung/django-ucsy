// Update the Total Price field whenever number of people changes
function updatePrice() {
    const people = parseInt(document.getElementById('people').value) || 1;
    const price = parseFloat(document.getElementById('pricePerSeat').value) || 0;
    const total = (people * price).toFixed(2);
    
    document.getElementById('totalPrice').value = 
        new Intl.NumberFormat('en-US', { 
            style: 'currency', 
            currency: 'MMK',
            minimumFractionDigits: 2
        }).format(total);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize price calculation
    updatePrice();
    
    // Add event listeners for all input types
    const peopleInput = document.getElementById('people');
    peopleInput.addEventListener('input', updatePrice);
    peopleInput.addEventListener('change', updatePrice);
    
    // Get modal instance
    const receiptModal = new bootstrap.Modal(document.getElementById('receiptConfirmationModal'));
    
    // Show receipt button click handler - ONLY VALIDATION, NO BOOKING CREATION
    document.getElementById('showReceiptBtn').addEventListener('click', function() {
        // Validate form
        const form = document.getElementById('bookingForm');
        form.classList.add('was-validated');
        
        if (!form.checkValidity()) {
            return;
        }
        
        // Get form values for modal display
        const formData = {
            name: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            people: parseInt(document.getElementById('people').value) || 1,
            packageTitle: '{{ package.title }}',
            departureDate: document.getElementById('tourDate').innerText,
            pricePerSeat: parseFloat(document.getElementById('pricePerSeat').value) || 0
        };
        
        // Calculate total
        const totalCost = (formData.people * formData.pricePerSeat).toFixed(2);
        
        // Populate modal with TEMPORARY data
        document.getElementById('receiptBookingId').textContent = 'TMP-' + Date.now();
        document.getElementById('receiptDate').textContent = new Date().toLocaleDateString();
        document.getElementById('receiptName').textContent = formData.name;
        document.getElementById('receiptEmail').textContent = formData.email;
        document.getElementById('receiptPhone').textContent = formData.phone;
        document.getElementById('receiptPackage').textContent = formData.packageTitle;
        document.getElementById('receiptDeparture').textContent = formData.departureDate;
        document.getElementById('receiptTravelers').textContent = formData.people;
        document.getElementById('receiptTotal').textContent = 
            new Intl.NumberFormat('en-US', { 
                style: 'currency', 
                currency: 'MMK',
                minimumFractionDigits: 2
            }).format(totalCost);
        
        // Show modal
        receiptModal.show();
    });
    
    // Final confirmation handler - ACTUAL BOOKING CREATION
    document.getElementById('confirmSaveBtn').addEventListener('click', function() {
        const form = document.getElementById('bookingForm');
        const formData = new FormData(form);
        
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
            if (data.error) throw new Error(data.error);
            
            // Update modal with REAL booking data from server
            if (data.booking_id) {
                document.getElementById('receiptBookingId').textContent = data.booking_id;
            }
            if (data.booking_date) {
                const bookingDate = new Date(data.booking_date);
                document.getElementById('receiptDate').textContent = bookingDate.toLocaleDateString();
            }
            
            // Show success message
            alert('Booking confirmed successfully!');
            
            // Hide modal after delay
            setTimeout(() => {
                receiptModal.hide();
                
                // Optional: Redirect to booking history or clear form
                
            }, 1500);
            
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Booking failed: ' + error.message);
        });
    });
});