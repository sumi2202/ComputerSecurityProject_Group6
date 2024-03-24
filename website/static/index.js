// login.html
document.addEventListener('DOMContentLoaded', function() {
    var loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        var student_id = document.getElementById('studentNumber').value;
        var password = document.getElementById('loginPassword').value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({student_id: student_id, password: password})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Go to download page for now
                window.location.href ='/profile_page';
            } else {
                throw new Error ('Login failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error during login:', error);
            alert(error.message);
        });

    });
});