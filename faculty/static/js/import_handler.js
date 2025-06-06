document.addEventListener("DOMContentLoaded", () => {
    const importBtn = document.getElementById("import-btn");
    const fileInput = document.getElementById("import-file");
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    const statusDiv = document.getElementById("import-status");
    const downloadLink = document.getElementById("download-failed"); // Create this in HTML

    if (!fileInput || !importBtn || !csrfToken || !statusDiv || !downloadLink) {
        console.error("Missing elements or CSRF token.");
        return;
    }

    function appendStatus(message) {
        statusDiv.textContent += message + "\n";
        statusDiv.scrollTop = statusDiv.scrollHeight;
    }

    importBtn.addEventListener("click", async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("📁 Please choose a file to import.");
            return;
        }

        statusDiv.textContent = "Starting import...\n";
        const reader = new FileReader();

        reader.onload = async (evt) => {
            const data = new Uint8Array(evt.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const worksheet = workbook.Sheets[workbook.SheetNames[0]];
            const rows = XLSX.utils.sheet_to_json(worksheet, { defval: "" });

            let successCount = 0;
            let failCount = 0;
            const failedRows = [];

            for (const [index, row] of rows.entries()) {
                appendStatus(`Importing row ${index + 1}...`);

                try {
                    const formData = new FormData();
                    formData.append('data', JSON.stringify(row));

                    const response = await fetch("/faculty/alumni-import", {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken,
                        },
                        body: formData,
                    });

                    const result = await response.json();

                    if (result.success) {
                        appendStatus(`✅ Row ${index + 1} imported successfully.`);
                        successCount++;
                    } else {
                        appendStatus(`❌ Row ${index + 1} failed: ${result.message || "Unknown error"}`);
                        failCount++;
                        failedRows.push({
                            Row: index + 1,
                            Email: row["Email Address"] || "N/A",
                            Reason: result.message || "Unknown error"
                        });
                    }
                } catch (err) {
                    appendStatus(`🚨 Error importing row ${index + 1}: ${err.message || err}`);
                    failCount++;
                    failedRows.push({
                        Row: index + 1,
                        Email: row["Email Address"] || "N/A",
                        Reason: err.message || "Unknown error"
                    });
                }
            }

            appendStatus(`\nImport completed: ${successCount} success, ${failCount} failed.`);

            if (failedRows.length > 0) {
                const worksheet = XLSX.utils.json_to_sheet(failedRows);
                const wb = XLSX.utils.book_new();
                XLSX.utils.book_append_sheet(wb, worksheet, "Failed Imports");

                const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
                const blob = new Blob([wbout], { type: "application/octet-stream" });
                const url = URL.createObjectURL(blob);

                downloadLink.href = url;
                downloadLink.download = "failed_imports.xlsx";
                downloadLink.style.display = "inline-block";
                downloadLink.textContent = "⬇️ Download Failed Rows";
            } else {
                downloadLink.style.display = "none";
            }
        };

        reader.readAsArrayBuffer(file);
    });
});
