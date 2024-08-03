document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript Loaded');  // Debug statement

    // Profile Form Handling
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        const updateProfileUrl = profileForm.getAttribute('data-update-url');
        const userProfileUrl = profileForm.getAttribute('data-user-profile-url');
        
        // Function to handle profile update
        profileForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting the traditional way

            var formData = new FormData(this);

            fetch(updateProfileUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'  // Add this header to indicate an AJAX request
                }
            })
            .then(response => {
                console.log('Response received:', response);  // Debug statement
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Data processed', data);  // Debug statement

                var messageDiv = document.getElementById('message');
                if (data.success) {
                    messageDiv.innerHTML = '<p>Profile updated successfully.</p>';
                    setTimeout(function() {
                        window.location.href = userProfileUrl; // Redirect to profile page after successful update
                    }, 1000);
                } else {
                    var errors = '';
                    for (var error in data.errors) {
                        errors += '<p>' + error + ': ' + data.errors[error] + '</p>';
                    }
                    messageDiv.innerHTML = errors;
                }
            })
            .catch(error => {
                console.error('Error:', error);  // Debug statement
            });
        });
    }

    // Function to handle event deletion
    function confirmDelete(event, eventId) {
        event.preventDefault();
        if (confirm('Are you sure you want to delete this event?')) {
            const deleteForm = document.getElementById(`delete-form-${eventId}`);
            fetch(deleteForm.action, {
                method: 'POST',
                body: new FormData(deleteForm),
                headers: {
                    'X-CSRFToken': deleteForm.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'  // Add this header to indicate an AJAX request
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log('Event deleted successfully.');
                    window.location.reload();  // Reload the page after successful deletion
                } else {
                    console.error('Error deleting event.');
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
        }
    }

    // Attach event deletion handler to all delete links
    const deleteLinks = document.querySelectorAll('.delete-event');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const eventId = this.getAttribute('data-event-id');
            confirmDelete(event, eventId);
        });
    });

    // Handle RSVP form submission
    const rsvpForm = document.getElementById('rsvp-form');
    if (rsvpForm) {
        rsvpForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const selectedStatus = document.querySelector('input[name="status"]:checked');
            if (!selectedStatus) {
                document.getElementById('rsvp-message').textContent = 'Please select an RSVP status.';
                return;
            }

            const status = selectedStatus.value;
            const url = rsvpForm.getAttribute('data-url');

            fetch(url, {
                method: 'POST',
                body: new URLSearchParams({
                    'status': status,
                    'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    document.getElementById('rsvp-message').textContent = 'RSVP updated successfully!';
                    // Optionally, reload the page to reflect changes
                    location.reload();
                } else {
                    document.getElementById('rsvp-message').textContent = 'Failed to update RSVP.';
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                document.getElementById('rsvp-message').textContent = 'Failed to update RSVP.';
            });
        });
    }

    // Fetch and display weather data based on user's geolocation
    function fetchWeatherByLocation(latitude, longitude) {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m&timezone=auto`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const temperature = data.hourly.temperature_2m[0];  // Adjust according to the API response
                document.getElementById('temperature').innerText = `${temperature}°C`;
                localStorage.setItem('temperature', temperature);
                localStorage.setItem('lastUpdated', new Date().getTime());
            })
            .catch(error => {
                console.error('Error fetching weather data:', error);
                document.getElementById('temperature').innerText = 'N/A';
            });
    }

    // Check if the temperature data is in localStorage and if it's fresh
    function checkTemperature() {
        const storedTemperature = localStorage.getItem('temperature');
        const lastUpdated = localStorage.getItem('lastUpdated');
        const TEN_MINUTES = 10 * 60 * 1000;

        if (storedTemperature && lastUpdated) {
            const now = new Date().getTime();
            if (now - lastUpdated < TEN_MINUTES) {
                document.getElementById('temperature').innerText = `${storedTemperature}°C`;
                return;
            }
        }

        // If data is not fresh, fetch new data
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                fetchWeatherByLocation(latitude, longitude);
            }, error => {
                console.error('Error getting geolocation:', error);
                document.getElementById('temperature').innerText = 'N/A';
            });
        } else {
            console.error('Geolocation is not supported by this browser.');
            document.getElementById('temperature').innerText = 'N/A';
        }
    }

    checkTemperature();

    // Toggle Filter Form Visibility
    const toggleFilterButton = document.getElementById('toggle-filter');
    const filterForm = document.getElementById('filter-form');

    if (toggleFilterButton && filterForm) {
        toggleFilterButton.addEventListener('click', function() {
            if (filterForm.style.display === 'none' || filterForm.style.display === '') {
                filterForm.style.display = 'block';
            } else {
                filterForm.style.display = 'none';
            }
        });
    }
});
