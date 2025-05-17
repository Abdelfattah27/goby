

  function updateFileName() {
    const fileInput = document.querySelector(".image_upload");
    const fileButtonText = document.getElementById("fileButtonText");
    const imagePreview = document.querySelector(".image_preview")

    if (fileInput.files.length > 0) {
      fileButtonText.textContent = fileInput.files[0].name;
       
        // Create a FileReader
        const reader = new FileReader();

        // Set an event handler for when the file is loaded
        reader.onload = function (e) {
          // Set the result as the src attribute of the image tag
          imagePreview.src = e.target.result;
        };

        // Read the selected file as a data URL
        reader.readAsDataURL(fileInput.files[0]);
    } else {
      fileButtonText.textContent = "Choose file";
    }
  }