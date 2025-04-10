document.addEventListener("DOMContentLoaded", function () {
    // Add click event listeners to all section headers
    document.querySelectorAll(".section-head").forEach(function (header) {
        header.addEventListener("click", function () {
            // Find the corresponding section body
            let body = this.nextElementSibling;

            // Check if the body has the class 'section-body'
            if (body && body.classList.contains("section-body")) {
                // Toggle the 'collapsed' class on the body
                body.classList.toggle("collapsed");

                // Toggle the 'collapsed' class on the header
                this.classList.toggle("collapsed");
            }
        });
    });
});