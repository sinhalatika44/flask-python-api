document.addEventListener('DOMContentLoaded', function() {
    const waitlistBtn = document.getElementById('waitlistBtn');
    const waitlistForm = document.querySelector('.waitlist-form');
    const form = document.getElementById('waitlistForm');

    waitlistBtn.addEventListener('click', function() {
        waitlistForm.style.display = 'block';
        waitlistBtn.style.display = 'none';
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;

        fetch('/api/waitlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            form.reset();
            waitlistForm.style.display = 'none';
            waitlistBtn.style.display = 'block';
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});