document.addEventListener('DOMContentLoaded', function() {
    const waitlistBtn = document.getElementById('waitlistBtn');
    const waitlistForm = document.querySelector('.waitlist-form');
    const form = document.getElementById('waitlistForm');
    const toast = document.getElementById('toast');
    const thankYouMessage = document.getElementById('thankYouMessage');

    if (waitlistBtn) {
        waitlistBtn.addEventListener('click', function() {
            waitlistForm.style.display = 'block';
            waitlistBtn.style.display = 'none';
        });
    }

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
            showToast(data.message);
            form.reset();
            waitlistForm.style.display = 'none';
            thankYouMessage.style.display = 'block';
            
            // Update the UI to reflect the user is now on the waitlist
            const ctaSection = document.querySelector('.cta');
            ctaSection.innerHTML = '<p class="waitlist-status">You\'re already on the waitlist!</p>';
        })
        .catch((error) => {
            console.error('Error:', error);
            showToast('An error occurred. Please try again.');
        });
    });

    function showToast(message) {
        toast.textContent = message;
        toast.classList.add('show');
        toast.style.display = 'block';
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.style.display = 'none';
            }, 300);
        }, 3000);
    }
});