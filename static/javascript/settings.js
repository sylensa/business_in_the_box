// Store initial input values
var initialValues = [];

document.getElementById("editButton").addEventListener("click", function() {
    var inputElements = document.querySelectorAll(".form-control");
    
    // Store initial values
    initialValues = Array.from(inputElements).map(function(inputElement) {
        return inputElement.value;
    });
    
    // Enable inputs for editing
    inputElements.forEach(function(inputElement) {
        inputElement.disabled = false;
    });
    
    // Show save and cancel buttons, hide edit button
    document.getElementById("editButton").style.display = "none";
    document.getElementById("saveButton").style.display = "inline-block";
    document.getElementById("cancelButton").style.display = "inline-block";
    alert("Please save or cancel your changes before leaving this page.");
});

document.getElementById("cancelButton").addEventListener("click", function() {
    var inputElements = document.querySelectorAll(".form-control");
    
    // Reset input values to initial values
    inputElements.forEach(function(inputElement, index) {
        inputElement.value = initialValues[index];
        inputElement.disabled = true;
    });
    
    // Hide save and cancel buttons, show edit button
    document.getElementById("editButton").style.display = "inline-block";
    document.getElementById("saveButton").style.display = "none";
    document.getElementById("cancelButton").style.display = "none";
    alert("Changes saved successfully.");
});
