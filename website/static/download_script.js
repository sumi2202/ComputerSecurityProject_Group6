document.addEventListener('DOMContentLoaded', function() {
    // Step 1: Reveal the login password form
    document.getElementById('download-doc-btn').addEventListener('click', function() {
        document.getElementById('verify-user').classList.remove('hidden');
    });

    // Step 2: Submit login password and reveal encryption password form
    document.getElementById('verify-user').addEventListener('submit', function(event) {
        event.preventDefault();
        const loginPassword = document.getElementById('login-password').value;
        fetch('/verify-user', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({loginPassword: loginPassword})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('encrypt-file').classList.remove('hidden');
            } else {
                alert('Invalid login password.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during verification.');
        });
    });

    // Step 3: Submit encryption password and enable download button
    document.getElementById('encrypt-file').addEventListener('submit', function(event) {
        event.preventDefault();
        const encryptPassword = document.getElementById('encrypt-password').value;
        fetch('/encrypt-report', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({reportPassword: encryptPassword})
        })
        .then(response => {
            if (response.ok) {
                document.getElementById('download-report-success-btn').classList.remove('hidden');
            } else {
                alert('Failed to encrypt the file.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during encryption.');
        });
    });

    // Step 4: Download the encrypted report
    document.getElementById('download-report-success-btn').addEventListener('click', function() {
        window.location.href = '/download-report'; // Initiating file download
    });
});
