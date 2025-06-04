document.addEventListener("DOMContentLoaded", () => {
    // 📥 Import Alumni File
    document.getElementById("import-btn").addEventListener("click", function () {
        const fileInput = document.getElementById("import-file");
        const file = fileInput.files[0];

        if (!file) {
            alert("Please choose a file to import.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        fetch("/import-alumni", {
            method: "POST",
            body: formData,
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    alert("Import successful!");
                    bootstrap.Modal.getInstance(
                        document.getElementById("import-modal")
                    ).hide();
                } else {
                    alert("Import failed: " + data.error);
                }
            })
            .catch((err) => {
                console.error(err);
                alert("An error occurred while importing the file.");
            });
    });
});
