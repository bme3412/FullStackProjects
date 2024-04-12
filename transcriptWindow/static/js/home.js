document.addEventListener("DOMContentLoaded", function () {
  // Handle form submission for file upload
  const uploadForm = document.getElementById("upload-form");
  const documentPlaceholder = document.getElementById("document-placeholder");
  const documentContent = document.getElementById("document-content");
  const messageElement = document.getElementById("message");
  const docWindow = document.querySelector(".document-window");

  if (uploadForm) {
    uploadForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData(this);

      fetch("/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            documentPlaceholder.style.display = "none";
            documentContent.innerHTML = data.content;
            console.log("Content loaded:", data.content); // Check what content is being injected
            adjustEmbedSize();
            if (messageElement) {
              messageElement.innerText = "";
            }
          } else {
            documentPlaceholder.style.display = "";
            documentPlaceholder.innerText = "File upload failed.";
            if (messageElement) {
              messageElement.innerText = data.message || "An error occurred.";
            }
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          if (messageElement) {
            messageElement.innerText = "Failed to fetch data.";
          }
        });
    });
  }

  // Function to adjust embed size after loading content
  function adjustEmbedSize() {
    const embed = docWindow.querySelector("embed");
    if (embed) {
      embed.onload = function () {
        this.style.width = "100%";
        this.style.height = "100%";
        console.log(
          "PDF fully loaded with dimensions:",
          this.offsetWidth,
          this.offsetHeight
        );
      };
      // Manually trigger size adjustment in case the embed is already loaded
      if (embed.complete) {
        embed.style.width = "100%";
        embed.style.height = "100%";
      }
    }
  }

  // Log initial dimensions
  console.log(
    "Initial Document window dimensions:",
    docWindow.offsetWidth,
    docWindow.offsetHeight
  );

  // Resize listener to log changes
  window.addEventListener("resize", function () {
    console.log(
      `Resize dimensions: ${docWindow.offsetWidth} x ${docWindow.offsetHeight}`
    );
  });

  // Initial size adjustment
  adjustEmbedSize();
});

// Dispatch a resize event shortly after loading to handle any asynchronous rendering issues
setTimeout(() => {
  window.dispatchEvent(new Event("resize"));
}, 1000); // Delay might need adjustment based on content loading times

function searchDocument() {
  const query = document.getElementById("search-query").value;
  const responseContent = document.getElementById("response-content");
  const documentContent = document.getElementById("document-content");
  const filename = document.getElementById("document").value.split("\\").pop(); // Get the filename from the file input

  fetch("/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, filename }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        responseContent.textContent = data.content;
        let attributionHtml = "";
        data.attribution.forEach((info) => {
          attributionHtml += `<p>Page ${info.page_number}:</p>`;
          attributionHtml += `<pre>${highlightText(
            info.text,
            data.termsToHighlight
          )}</pre>`; // Now dynamically highlighting based on backend analysis
        });
        documentContent.innerHTML = attributionHtml;
      } else {
        responseContent.textContent = "No results found.";
        documentContent.innerHTML = "";
      }
    })

    .catch((error) => {
      console.error("Error:", error);
      responseContent.textContent = "An error occurred during the search.";
      documentContent.innerHTML = "";
    });
}

function highlightText(text, termsToHighlight) {
  termsToHighlight.forEach((term) => {
    const regex = new RegExp(term, "gi"); // Ensure case-insensitive matching
    text = text.replace(regex, "<mark>$&</mark>");
  });
  return text;
}
