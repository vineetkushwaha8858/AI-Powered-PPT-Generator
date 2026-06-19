// // const API_URL = "http://192.168.1.185:8080/generate-presentation/";
// const API_URL = "http://129.154.244.67:6010/generate-download/";
// const API_URL = "http://localhost:8080/generate-presentation/";
const API_URL = "http://127.0.0.1:8000/generate-presentation";


document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("presentation-form");
  const loadingElem = document.getElementById("loading");
  const generateBtn = document.getElementById("generate-btn");
  const downloadBtn = document.getElementById("download-btn");
  const styleTiles = document.querySelectorAll('.style-tile');
  const templateNumberInput = document.getElementById('template_number');

  // Template selection logic
  styleTiles.forEach(tile => {
    tile.addEventListener('click', () => {
      styleTiles.forEach(t => t.classList.remove('selected'));
      tile.classList.add('selected');
      templateNumberInput.value = tile.dataset.value;
    });
  });

  // Form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // Show loading, hide download button
    loadingElem.style.display = "block";
    downloadBtn.style.display = "none";
    generateBtn.disabled = true;
    generateBtn.textContent = "Generating...";

    try {
      // Use FormData instead of URLSearchParams for multipart/form-data
      const formData = new FormData();
      formData.append("template_number", templateNumberInput.value);
      formData.append("topic", document.getElementById("topic").value.trim());
      formData.append("num_slides", document.getElementById("num-slides").value);
      formData.append("voice", document.getElementById("voice").value);
      formData.append("delay_between_slides", document.getElementById("delay_between_slides").value);
      
      // Convert boolean string to actual boolean for FormData
      const removeWatermarks = document.getElementById("remove_watermarks").value === "true";
      formData.append("remove_watermarks", removeWatermarks);

      // Make API request with FormData (no Content-Type header needed)
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to generate presentation: ${errorText}`);
      }

      // Get filename from response headers
      const contentDisposition = response.headers.get("content-disposition");
      let filename = "presentation.pptx";
      if (contentDisposition) {
        const match = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
        if (match && match[1]) {
          filename = match[1].replace(/['"]/g, '');
        }
      }

      // Create download link
      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      downloadBtn.href = objectUrl;
      downloadBtn.download = filename;
      downloadBtn.style.display = "block";
      
      generateBtn.textContent = "✅ Generated Successfully!";
      generateBtn.style.background = "#28a745";

    } catch (error) {
      console.error("Error:", error);
      alert("Error: " + error.message);
      generateBtn.textContent = "❌ Error - Try Again";
      generateBtn.style.background = "#dc3545";
    } finally {
      loadingElem.style.display = "none";
      setTimeout(() => {
        generateBtn.disabled = false;
        generateBtn.textContent = "Generate Presentation";
        generateBtn.style.background = "linear-gradient(90deg,#262328,#8bc1e8)";
      }, 3000);
    }
  });
});



















