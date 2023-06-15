function generateDocument() {
    const form = document.getElementById("generate_document_form");
    const formData = new FormData(form);

    fetch('/generate_document', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {

                    alert('Document generated successfully!');
                    updateLastUsedDates();
                } else {

                    alert('An error occurred while generating the document.');
                }
            })
            .catch(error => {
                alert('An error occurred while generating the document.');
                console.error(error);
            });
        }

        function updateLastUsedDates() {
            const checkboxes = document.querySelectorAll('input[name="question"]:checked');
            const questionIds = Array.from(checkboxes).map(checkbox => checkbox.value);

            questionIds.forEach(questionId => {
                const lastUsedElement = document.getElementById("last_used_" + questionId);
                const now = new Date();
                const formattedDate = now.toISOString().slice(0, 19).replace('T', ' ');
                lastUsedElement.textContent = formattedDate;
            });
        }