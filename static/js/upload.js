// $(document).ready(function() {
//     $('#submitBtn').click(function(e) {
//         e.preventDefault();
//         var formData = new FormData($('#uploadForm')[0]);
//         $.ajax({
//             url: '/upload',
//             type: 'POST',
//             data: formData,
//             contentType: false,
//             processData: false,
//             success: function(data) {
//                 $('#output').html('Recognized Text: ' + data.message);
//             },
//             error: function() {
//                 $('#output').html('Error in file processing');
//             }
//         });
//     });
// });

$(document).ready(function() {
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        var loadingElement = $('#loadingAnimation');
        var formData = new FormData(this);
        console.log(formData)
        loadingElement.show();
        $.ajax({
            url: '/upload',  // This should match the Flask route for file processing
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                loadingElement.hide();
                // Displaying both OCR and generated output
                $('#ocrOutput').html('OCR Text: ' + data.message);
                $('#generatedOutput').html('Generated Output: ' + data.generated_output);
            },
            error: function() {
                $('#output').html('Error in file processing');
            }
        });
        loadingElement.style.display = 'none';
    });
});
