// JavaScript code to handle the click count
let count = 0; // Initialize click count to 0
const button = document.getElementById('counterButton'); // Get the button element
const displayCount = document.getElementById('clickCount'); // Get the display element for the count

button.addEventListener('click', function () { // Add click event listener to the button
    count++; // Increment the count on each click
    displayCount.textContent = count; // Update the display with the new count
});