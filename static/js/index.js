// script.js

document.getElementById('crimeReportForm').addEventListener('submit', function(event) {
    event.preventDefault();

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

    function addIpcSectionsCheckboxes(ipcSections) {
        const container = document.getElementById('ipc-sections-container');
        container.innerHTML = ''; // Clear existing content
    
        ipcSections.forEach(section => {
            // Create checkbox
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'form-check-input'; // Bootstrap class
            checkbox.id = section; // Unique ID for the checkbox
            checkbox.name = 'ipcSections';
            checkbox.value = section;
    
            // Create label
            const label = document.createElement('label');
            label.className = 'form-check-label'; // Bootstrap class
            label.htmlFor = section; // Associate label with checkbox
            label.appendChild(document.createTextNode(section));
    
            // Wrap checkbox and label in a div
            const wrapper = document.createElement('div');
            wrapper.className = 'form-check';
            wrapper.appendChild(checkbox);
            wrapper.appendChild(label);
    
            container.appendChild(wrapper);
        });
    }
    
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
        // body: JSON.stringify({ reportedCrime: reportedCrime }),
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('firNoForIpc').value = formData.firNo;
        console.log(typeof data.result);
        var output = document.getElementById('reportOutput');
        loadingElement.style.display = 'none';
        addIpcSectionsCheckboxes(data.result);
        if (output) {
            output.innerHTML = '<h4>Applicable IPC Sections are as follows:</h4>' + data.result;  
            output.style.display = 'block'; 
        }
    })
    .catch(error => {
        loadingElement.style.display = 'none';
        console.error('Error:', error);
    });
    
});

// Handle the IPC sections form submission
document.getElementById('ipcSectionsForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the FIR number and the selected IPC sections
    var firNo = document.getElementById('firNoForIpc').value;
    var checkedIpcSections = Array.from(document.querySelectorAll('#ipcSectionsForm input[name="ipcSections"]:checked')).map(checkbox => checkbox.value);

    // Send the FIR number and IPC sections to the server
    fetch('/submit_ipc_sections', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            firNo: firNo,
            ipcSections: checkedIpcSections.join(', ')
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(firNo)
        if(data.status === 'success') {
            window.location.href = `/display_fir/${firNo}`;
        } else {
            // Handle cases where the server response indicates failure
            console.error('Failed to submit IPC Sections:', data.message);
        }
    })
    .catch(error => {
        // Handle errors
        console.error('Error:', error);
    });
});

    // function addIpcSectionsCheckboxes(ipcSections) {
    //     const container = document.getElementById('ipc-sections-container'); // Replace with your actual container ID
    //     container.innerHTML = ''; // Clear existing content
    
    //     ipcSections.forEach(section => {
    //         const checkbox = document.createElement('input');
    //         checkbox.type = 'checkbox';
    //         checkbox.name = 'ipcSections';
    //         checkbox.value = section;
    
    //         const label = document.createElement('label');
    //         label.appendChild(checkbox);
    //         label.appendChild(document.createTextNode(section));
    
    //         container.appendChild(label);
    //         container.appendChild(document.createElement('br'));
    //     });
    // }    


