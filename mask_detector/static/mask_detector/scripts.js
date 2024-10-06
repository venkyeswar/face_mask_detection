document.addEventListener("DOMContentLoaded", function() {
    const resultText = document.querySelector(".result p"); // Adjust selector based on structure
    const uploadedImage = document.querySelector(".uploaded-image img");

    if (resultText) {
        const prediction = resultText.textContent.split(':')[1].trim();  // Extract label

        if (prediction === "With Mask") {
            resultText.style.color = "green";
            resultText.parentElement.style.backgroundColor = "#e0f7e0"; 
            uploadedImage.style.border = "5px solid green"; 
        } else if (prediction === "Without Mask") {
            resultText.style.color = "red";
            resultText.parentElement.style.backgroundColor = "#f8d7da"; 
            uploadedImage.style.border = "5px solid red"; 
        }
    }
});
