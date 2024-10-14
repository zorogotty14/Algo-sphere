document.addEventListener("DOMContentLoaded", function () {
    // Fetch explanation and code dynamically from the server
    fetch('/get_bubble_sort_info')  // Adjust URL as per your Flask route
        .then(response => response.json())
        .then(data => {
            // Populate explanation
            document.getElementById("explanation-text").textContent = data.explanation;

            // Populate code block
            document.getElementById("code-block").textContent = data.code;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById("explanation-text").textContent = "Error loading explanation.";
            document.getElementById("code-block").textContent = "Error loading code.";
        });
});
