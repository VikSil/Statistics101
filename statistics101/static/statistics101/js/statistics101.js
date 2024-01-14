// Main file containing all async functions for extracting data
// For data upload via Dropzone.js - see userdata.js

// Once the HTML has loaded
document.addEventListener("DOMContentLoaded", function () {
  // On resize - if large screen then always show menu pane
  addEventListener("resize", adjust_layout);

  // Add listener to all inbuilt dataset display buttons
  const showDatasetBtns = document.getElementsByClassName("dataset-btn");
  showDatasetBtns.forEach((button) => {
    button.addEventListener("click", displayDataset);
  });

  // Add listener to all user dataset delete buttons
  const delUsrDatasetBtns = document.getElementsByClassName(
    "owned-dataset-delete"
  );
  delUsrDatasetBtns.forEach((button) => {
    button.addEventListener("click", deleteDataset);
  });

  // Add listener to all buttons in Statistics
  const showStatsBtns = document.getElementsByClassName("statistics-btn");
  showStatsBtns.forEach((button) => {
    button.addEventListener("click", displayStatistics);
  });

  // Add listener to all buttons in Charts
  const showChartBtns = document.getElementsByClassName("chart-btn");
  showChartBtns.forEach((button) => {
    button.addEventListener("click", displayCharts);
  });

  // On page load adjust layout according to screen size
  adjust_layout();
});

//----------------------------------------------------
// Function to extract CSRF token from cookies, as per DJANGO documentation
// https://docs.djangoproject.com/en/3.2/ref/csrf/
//----------------------------------------------------
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Adjust the layout to show menu on resize
function adjust_layout() {
  // Get the Div that contains the offcanvas menu
  const menu = document.getElementById("floating-menu");
  // Get the div that contains the main text area
  const main = document.getElementById("main-area");

  // If large screen - show the menu; it has no close button on the large screen
  let width = window.innerWidth;
  // On large screen
  if (width >= 992) {
    // Show menu
    menu.classList.add("show");
    // Adjust left  margin of the main text area to the size of the menu
    main.style.marginLeft = `${menu.offsetWidth}px`;
  }
  // On less than large screen
  else {
    // Hide menu
    menu.classList.remove("show");
    // Adjust the left margin for the main text area to fill the entire screen
    main.style.marginLeft = "0px";
  }
}

// Get dataset and display in table
async function displayDataset() {
  // Get the div where the table will be displayed
  const dataDiv = document.querySelector(this.dataset.datadiv);
  // Temporary waiting message
  dataDiv.innerHTML =
    'Fetching dataset, please wait...<br><div class="spinner-border text-plumdark" role="status"><span class="visually-hidden">Loading...</span></div>';

  // Prepare and send GET request
  url = `/statistics101/dataset=${this.dataset.sampleid}&func=get_dataset`;
  const response = await fetch(url);
  let html = "";
  if (response.status === 200) {
    // If successfull request, extract html from response
    html = await response.text();
  } else {
    // If failed to retrieve the dataset, will display error
    html = "<p>Something went wrong. Please try again later.</p>";
  }
  // Replace the waiting placeholder with response/error
  dataDiv.innerHTML = html;
}

// Delete a dataset
async function deleteDataset() {
  // Strip dataset name off of the button dataset
  const sampleName = this.dataset.samplename;
  // Find DOM elements that allows user to interact with the dataset
  const datasetBtn = document.getElementById(sampleName);
  const dataDiv = document.getElementById(this.dataset.datadiv);
  // Hide those elements
  dataDiv.innerHTML = "";
  datasetBtn.remove();
  this.remove();

  // Prepare request to remove a dataset
  const url = `/statistics101/userdata`;
  let json = { sampleid: this.dataset.sampleid };
  let obj = JSON.stringify(json);
  const csrftoken = getCookie("csrftoken");

  // send PUT request
  fetch(url, {
    method: "PUT",
    body: obj,
    headers: { "X-CSRFToken": csrftoken },
  })
    .then((response) => {
      //When response is received
      localStorage.clear();
      if (response.status === 204) {
        // If successfull request, tell the user
        alert(`Dataset ${sampleName} was deleted`);
      }
      // If failed request, also tell user
      else {
        alert(
          `Something wrong when deleting ${sampleName}. Refresh the page and try again.`
        );
      }
    })
    // If unexpected error, log the error and tell the user
    .catch((err) => {
      console.log(
        err,
        "<-- need to debug this failed PUT request to /userdata"
      );
      alert(
        `Something wrong when deleting ${sampleName}. Refresh the page and try again.`
      );
    });
}

// Get the statistic for a dataset and display in table
async function displayStatistics() {
  // Get the div where the table will be displayed
  const dataDiv = document.querySelector(this.dataset.datadiv);
  // Temporary waiting message
  dataDiv.innerHTML =
    'Fetching dataset, please wait...<br><div class="spinner-border text-plumdark" role="status"><span class="visually-hidden">Loading...</span></div>';

  // Prepare and send GET request - parameters come from the button that was pressed
  const url = `/statistics101/dataset=${this.dataset.sampleid}&func=${this.dataset.f}`;
  const response = await fetch(url);
  let html = "";
  if (response.status === 200) {
    // If successfull request, extract html from response
    html = await response.text();
  }
  // If failed to retrieve the statistics, will display error
  else {
    html = "<p>Something went wrong. Please try again later.</p>";
  }
  // Replace the waiting placeholder with response/error
  dataDiv.innerHTML = html;
}

// Get a Plotly chart as html
async function displayCharts() {
  // Get the div where the chart will be displayed
  const someDIV = document.getElementById(this.dataset.chartarea);
  // Temporary waiting message
  someDIV.innerHTML =
    'Fetching dataset, please wait...<br><div class="spinner-border text-plumdark" role="status"><span class="visually-hidden">Loading...</span></div>';

  // Prepare and send GET request - parameters come from the button that was pressed
  url = `/statistics101/chart=${this.dataset.sampleid}&func=${this.dataset.f}`;
  const response = await fetch(url);

  // If successfull request
  if (response.status === 200) {
    // Extract html from response
    let data = await response.text();
    // Wrap the chart in a parent div
    data = `<div id = "${this.dataset.chartarea}">` + data + "</div>";
    // Remove waiting message
    someDIV.remove();
    // Add the chart to the page
    const chartDIV = document.getElementById(this.dataset.chartdiv);
    let frag = document.createRange().createContextualFragment(data);
    chartDIV.appendChild(frag);
  }

  // If failed to retrieve the statistics, will display error
  else {
    let html = "<p>Something went wrong. Please try again later.</p>";
    // Replace the waiting placeholder with error
    someDIV.innerHTML = html;
  }
}
