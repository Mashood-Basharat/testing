document.getElementById('signupForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the form from submitting normally

    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!firstName || !lastName || !email || !password) {
        alert('Please fill out all fields.');
        return;
    }

    // Email format validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    // Simulate an AJAX request
    // fetch('/signup', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({ firstName, lastName, email, password })
    // })
    //     .then(response => {
    //         if (response.ok) {
    //             window.location.href = 'login.html'; // Redirect on success
    //         } else {
    //             alert('An error occurred. Please try again later.');
    //         }
    //     })
    //     .catch(error => {
    //         console.error('Error:', error);
    //         alert('An error occurred. Please try again later.');
    //     });

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ firstName, lastName, email, password })
    })
        .then(response => response.json())
        .then(data => {
            if (response.ok) {
                window.location.href = 'login'; // Use your actual login route here
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });
    
});
