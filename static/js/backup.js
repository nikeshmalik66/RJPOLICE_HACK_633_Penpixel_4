// script.js

document.getElementById('crimeReportForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Collect form data
    var formData = {
        firNo: document.getElementById('firNo').value,
        district: document.getElementById('district').value,
        date: document.getElementById('date').value,
        day: document.getElementById('day').value,
        dateOfOccurrence: document.getElementById('dateOfOccurrence').value,
        placeOfOccurrence: document.getElementById('placeOfOccurrence').value,
        name: document.getElementById('name').value,
        dob: document.getElementById('dob').value,
        nationality: document.getElementById('nationality').value,
        occupation: document.getElementById('occupation').value,
        address: document.getElementById('address').value,
        reportedCrime: document.getElementById('reportedCrime').value,
        propertiesInvolved: document.getElementById('propertiesInvolved').value
    };

    // Display the data in the output section
    // var output = document.getElementById('reportOutput');
    // output.innerHTML = '<h4>Submitted Report:</h4>' + JSON.stringify(formData, null, 4);
    // output.style.display = 'block'; // Make the output section visible   
});

document.getElementById('crimeReportForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Show loading animation
    var loadingElement = document.getElementById('loadingAnimation');
    loadingElement.style.display = 'block';

    // Get the reported crime data
    var reportedCrime = document.getElementById('reportedCrime').value;
    console.log(reportedCrime)
    // AJAX request to the Flask route
    fetch('/process_reported_crime', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ reportedCrime: reportedCrime })
    })
    fetch('/submit_report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...formData, modelOutput: data.result })
    })
    .then(response => response.json())
    .then(data => {
        var output = document.getElementById('reportOutput');
        loadingElement.style.display = 'none';
        if (output) {
            output.innerHTML = '<h4>AI Model Output:</h4>' + data.result;  // Assuming 'data.result' is the key for the output string
            output.style.display = 'block';
        }
    })
    .catch(error => {
        loadingElement.style.display = 'none';
        console.error('Error:', error);
    });
    
});
