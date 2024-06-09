document.getElementById('patient-registration-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = {
        firstName: document.getElementById('first-name').value,
        lastName: document.getElementById('last-name').value,
        maritalStatus: document.getElementById('marital-status').value,
        gender: document.querySelector('input[name="gender"]:checked').value,
        password: document.getElementById('password').value,
        homeAddress: document.getElementById('home-address').value
    };

    console.log('Form Data Submitted:', formData);
    // Here you would typically send the form data to the server using fetch or AJAX
    // fetch('your-server-endpoint', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify(formData)
    // })
    // .then(response => response.json())
    // .then(data => console.log(data))
    // .catch(error => console.error('Error:', error));
});
