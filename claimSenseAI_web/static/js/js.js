window.addEventListener("load", function() {
        const claimInput = document.getElementById("claim_pdf");
        const claimFileList = document.getElementById("claim_file_list");  // Fix: Get the correct element

        const policyInput = document.getElementById("policy_pdf");
        const policyFileList = document.getElementById("policy_file_list");  // Fix: Get the correct element

        const input_warning = document.getElementById("input_warning");
        const prompt_input = document.getElementById("prompt");

        prompt_input.addEventListener("input", function() {
                if (prompt_input.value.trim() !== "") {
                        input_warning.classList.add("hidden");
                } else {
                        input_warning.classList.remove("hidden");
                }
        });

        const file_warning = document.getElementById("file_warning");

        function checkFiles() {
                // Check if both inputs have files selected
                if (claimInput.files.length > 0 && policyInput.files.length > 0) {
                        file_warning.classList.add("hidden"); // Hide warning
                } else {
                        file_warning.classList.remove("hidden"); // Show warning if any input is empty
                }
        }

        function updateFileList(input, fileListElement) {
                fileListElement.innerHTML = ''; // Clear the previous list
                if (input.files.length > 0) {
                        for (const file of input.files) {
                                const listItem = document.createElement('li');
                                listItem.textContent = file.name;
                                fileListElement.appendChild(listItem);
                        }
                } else {
                        const listItem = document.createElement('li');
                        listItem.textContent = "No File Chosen";
                        fileListElement.appendChild(listItem);
                }
        }

        // Listen for changes in both file inputs
        claimInput.addEventListener("change", function() {
                checkFiles();
                updateFileList(claimInput, claimFileList);  // Fix: Pass correct element
        });

        policyInput.addEventListener("change", function() {
                checkFiles();
                updateFileList(policyInput, policyFileList);  // Fix: Pass correct element
        });

        const form = document.getElementById("form_post");
        const loadingBar = document.getElementById("load_bar");

        form.addEventListener("submit", function () {
                // Show the loading bar
                loadingBar.classList.remove("hidden");
                // Allow the form to submit normally
        });

        const navigation = performance.getEntriesByType("navigation");
        if (navigation.length > 0 && navigation[0].type === "reload") {
                loadingBar.classList.add("hidden");
        }
        window.addEventListener('load', () => {
                loadingBar.classList.add("hidden");  // Hide when the new page has loaded
        });
});
