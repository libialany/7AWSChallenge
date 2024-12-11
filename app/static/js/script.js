document.getElementById('submitBtn').addEventListener('click', function() {
    var selectedOption = document.getElementById('dropdown').value;
    
    if (selectedOption) {
        var iframe = document.getElementById('iframe');
        iframe.src = selectedOption;
    } else {
        alert("Please select a page to display.");
    }
});
