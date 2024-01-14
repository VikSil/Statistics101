// Configuration for data upload via Dropzone.js
// For async functions for extracting data - see statistics101.js

// Once the HTML has loaded
document.addEventListener("DOMContentLoaded", function () {
  // Configure all dropzones
  Dropzone.options.TimeseriesDropzone = {
    paramName: "timeseries", // this allows to access the file for *this particular* dropzone
    maxFiles: 1,
    maxFilesize: 3,
    acceptedFiles: ".csv",
    autoProcessQueue: true, // if false stops from uploading files until user submits form
    clickable: true, // invoke os file choose window
    withCredentials: true,

    init: function () {
      // Once bitestream of the file has been received
      this.on("success", function (file) {
        if (
          // No more files in the queue
          this.getUploadingFiles().length === 0 &&
          this.getQueuedFiles().length === 0
        ) {
          // Notify user
          alert("File has been received and will be processed shortly.");
          // Invoke async file checks and processing
          processfile(file.name);
        }
      });
    },
  };

  Dropzone.options.ProportionDropzone = {
    paramName: "proportion", // this allows to access the file for *this particular* dropzone
    maxFiles: 1,
    maxFilesize: 3,
    acceptedFiles: ".csv",
    autoProcessQueue: true, // if false stops from uploading files until user submits form
    clickable: true, // invoke os file choose window

    init: function () {
      // Once bitestream of the file has been received
      this.on("success", function (file) {
        if (
          // No more files in the queue
          this.getUploadingFiles().length === 0 &&
          this.getQueuedFiles().length === 0
        ) {
          // Notify user
          alert("File has been received and will be processed shortly.");
          // Invoke async file checks and processing
          processfile(file.name);
        }
      });
    },
  };

  Dropzone.options.SurveyDropzone = {
    paramName: "survey", // this allows to access the file for *this particular* dropzone
    maxFiles: 1,
    maxFilesize: 3,
    acceptedFiles: ".csv",
    autoProcessQueue: true, // if false stops from uploading files until user submits form
    clickable: true, // invoke os file choose window

    init: function () {
      // Once bitestream of the file has been received
      this.on("success", function (file) {
        if (
          // No more files in the queue
          this.getUploadingFiles().length === 0 &&
          this.getQueuedFiles().length === 0
        ) {
          // Notify user
          alert("File has been received and will be processed shortly.");
          // Invoke async file checks and processing
          processfile(file.name);
        }
      });
    },
  };
});

// Function to invoke file checks, processing and saving of the data
async function processfile(filename) {
  // Prepare POST request
  const url = `/statistics101/processfile`;
  let json = { filename: filename };
  let obj = JSON.stringify(json);
  const csrftoken = getCookie("csrftoken");

  // send POST request
  fetch(url, {
    method: "POST",
    body: obj,
    headers: { "X-CSRFToken": csrftoken },
  })
    .then((response) => {
      //When response is received
      if (response.status === 201) {
        // If successful - notify user (only visible if user has not exited the template)
        alert(`File ${filename} has been processed successfully.`);
      }
      // If POST returns an error - notify user  (only visible if user has not exited the template)
      else {
        alert(
          `Something went wrong when processing ${filename}. Please check file format and sample limit.`
        );
      }
    })
    // If an issue with this function- notify user  (only visible if user has not exited the template)
    .catch((err) => {
      alert(`File ${filename} upload failed. Error: ${err}`);
    });
}
