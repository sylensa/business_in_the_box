// Store initial input values
var initialValues = {};

// Get reference to the form element
var form = document.getElementById("myForm");

// Get reference to the external button
var externalButton = document.getElementById("saveButton");

// Attach click event listener to the external button
externalButton.addEventListener("click", function() {
  // Submit the form
//   alert("Changes saved successfully.");
  form.submit();
});

document.getElementById("editButton").addEventListener("click", function() {
    var inputElements = document.querySelectorAll(".form-control");
    var selectElements = document.querySelectorAll(".from-control");
    
    // Store initial values for inputs
    inputElements.forEach(function(inputElement) {
        initialValues[inputElement.name] = inputElement.value;
    });

    // Store initial values for selects
    selectElements.forEach(function(selectElement) {
        initialValues[selectElement.name] = selectElement.value;
    });

    // Enable inputs and selects for editing
    inputElements.forEach(function(inputElement) {
        inputElement.disabled = false;
    });
    selectElements.forEach(function(selectElement) {
        selectElement.disabled = false;
    });

    // Show save and cancel buttons, hide edit button
    document.getElementById("editButton").style.display = "none";
    document.getElementById("saveButton").style.display = "inline-block";
    document.getElementById("cancelButton").style.display = "inline-block";
    alert("Please save or cancel your changes before leaving this page.");
});

document.getElementById("cancelButton").addEventListener("click", function() {
    var inputElements = document.querySelectorAll(".form-control");
    var selectElements = document.querySelectorAll(".form-control");
    
    // Reset input values to initial values
    inputElements.forEach(function(inputElement) {
        inputElement.value = initialValues[inputElement.name];
        inputElement.disabled = true;
    });

    // Reset select values to initial values
    selectElements.forEach(function(selectElement) {
        selectElement.value = initialValues[selectElement.name];
        selectElement.disabled = true;
    });

    // Hide save and cancel buttons, show edit button
    document.getElementById("editButton").style.display = "inline-block";
    document.getElementById("saveButton").style.display = "none";
    document.getElementById("cancelButton").style.display = "none";
    alert("Changes canceled successfully.");
});

document.getElementById("saveButton").addEventListener("click", function() {
    var inputElements = document.querySelectorAll(".form-control");
    var selectElements = document.querySelectorAll(".textField");
    
    // Reset input values to initial values
    inputElements.forEach(function(inputElement) {
        inputElement.disabled = true;
    });

    // Reset select values to initial values
    selectElements.forEach(function(selectElement) {
        selectElement.disabled = true;
    });

    // Hide save and cancel buttons, show edit button
    document.getElementById("editButton").style.display = "inline-block";
    document.getElementById("saveButton").style.display = "none";
    document.getElementById("cancelButton").style.display = "none";
    // alert("Changes saved successfully.");
});
