// Initialize when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize price calculation
    updatePrice();
    
    // Setup modal instance
    const receiptModal = new bootstrap.Modal(
        document.getElementById('receiptConfirmationModal'), 
        { keyboard: false }
    );

    // 1. Handle "Confirm Booking" button click to SHOW the popup
    document.getElementById('showReceiptBtn').addEventListener('click', function() {
        // Validate form
        const form = document.getElementById('bookingForm');
        form.classList.add('was-validated');
        
        if (!form.checkValidity()) {
            // If form is invalid, highlight errors but don't show modal
            return;
        }

        // Get all form values
        const formData = {
            name: document.getElementById('fullName').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            people: parseInt(document.getElementById('people').value) || 1,
            packageTitle: '{{ package.title }}', // From Django template
            departureDate: document.getElementById('tourDate').innerText,
            pricePerSeat: parseFloat(document.getElementById('pricePerSeat').value) || 0
        };

        // Calculate total
        const totalCost = (formData.people * formData.pricePerSeat).toFixed(2);
        
        // 2. Populate the modal with booking info
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

        // 3. Show the modal
        receiptModal.show();
    });

    // 4. Handle "Confirm" button INSIDE the popup to SAVE the booking
    document.getElementById('confirmSaveBtn').addEventListener('click', function() {
        const form = document.getElementById('bookingForm');
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(async response => {
            // First check if response is JSON
            const contentType = response.headers.get('content-type');
            const responseText = await response.text();
            
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error(`Expected JSON but got: ${responseText.substring(0, 100)}...`);
            }
            
            return JSON.parse(responseText);
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Update with real booking ID from server
            if (data.booking_id) {
                document.getElementById('receiptBookingId').textContent = data.booking_id;
            }
            
            // Show success message
            alert('Booking confirmed! ID: ' + (data.booking_id || 'Pending'));
            
            // Hide the modal
            receiptModal.hide();
            
            // Reset form (optional)
            form.reset();
            updatePrice();
        })
        .catch(error => {
            console.error('Booking error:', error);
            alert('Booking failed: ' + error.message);
        });
    });

    // Setup price calculation when people changes
    document.getElementById('people').addEventListener('change', updatePrice);
});

// Price calculation function
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