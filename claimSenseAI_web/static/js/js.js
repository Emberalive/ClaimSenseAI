window.addEventListener("load", function() {
        const claimInput = document.getElementById("claim_pdf");
        const claimFileName = document.getElementById("claim_file_name");

        const policyInput = document.getElementById("policy_pdf");
        const policyFileName = document.getElementById("policy_file_name");

        const input_warning = document.getElementById("input_warning");
        const prompt_input = document.getElementById("prompt");

        prompt_input.addEventListener("input", function() {
                if (prompt_input.value.trim() !== "") {
                        input_warning.classList.add("hidden");
                } else {
                        input_warning.classList.remove("hidden");
                }
        })


        const file_warning = document.getElementById("file_warning");

        function checkFiles() {
                // Check if both inputs have files selected
                if (claimInput.files.length > 0 && policyInput.files.length > 0) {
                        file_warning.classList.add("hidden"); // Add the class to hide the warning
                } else {
                        file_warning.classList.remove("hidden"); // Show the warning if any input is empty
                }
        }

        function updateFileName(input, displayElement) {
                if (input.files.length > 0) {
                        displayElement.textContent = input.files[0].name;
                } else {
                        displayElement.textContent = "No file chosen";
                }
        }


        // Listen for changes in both file inputs
        claimInput.addEventListener("change", function() {
                checkFiles();
                updateFileName(claimInput, claimFileName);
        });

        policyInput.addEventListener("change", function() {
                checkFiles();
                updateFileName(policyInput, policyFileName)
        });

        const form = document.getElementById("form_post");
        const loadingBar = document.getElementById("load_bar");

        form.addEventListener("submit", function () {
                // Show the loading bar
                loadingBar.classList.remove("hidden");
                // Allow the form to submit normally
                // The loading bar will be visible until the page redirects
        });

        const navigation = performance.getEntriesByType("navigation");
        if (navigation.length > 0 && navigation[0].type === "reload") {
                loadingBar.classList.add("hidden");
                if (navigation.length > 0 && navigation[0].type === "none") {
                        loadingBar.classList.add("hidden");
                }
        }
        window.addEventListener('load', () => {
                loadingBar.classList.add("hidden");  // Hide when the new page has loaded
        });
});
