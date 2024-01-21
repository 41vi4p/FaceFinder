const dropArea = document.querySelector(".js-drop-area");
const dropContent = document.querySelector(".js-drop-content");
const dropResult = document.querySelector(".js-drop-result");
const dropInput = document.querySelector(".js-input-file");

var delayInMilliseconds = 1000; //1 second


dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
});

dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropInput.files =  e.dataTransfer.files;
  dropContent.classList.remove("active");
  $(".done").show().addClass("animated zoomIn");
  //dropResult.classList.add("active");
  console.log(dropInput.files);
  
});

dropInput.addEventListener("change", (e) => {
  e.preventDefault();
  dropContent.classList.remove("active");
  $(".done").show().addClass("animated zoomIn");
  dropResult.classList.add("done");
  console.log(e.target.files);
  
});



// select the second drop area and its elements
const dropArea2 = document.querySelector(".js-drop-area-2");
const dropContent2 = document.querySelector(".js-drop-content-2");
const dropResult2 = document.querySelector(".js-drop-result-2");
const dropInput2 = document.querySelector(".js-input-file-2");

// add the same event listeners as the first drop area
dropArea2.addEventListener("dragover", (e) => {
  e.preventDefault();
});

dropArea2.addEventListener("drop", (e) => {
  e.preventDefault();
  dropInput2.files =  e.dataTransfer.files;
  dropContent2.classList.remove("active");
  $(".done-2").show().addClass("animated zoomIn");
  //dropResult2.classList.add("active");
  console.log(dropInput2.files);
});

dropInput2.addEventListener("change", (e) => {
  e.preventDefault();
  dropContent2.classList.remove("active");
  $(".done-2").show().addClass("animated zoomIn");
  //dropResult2.classList.add("done");
  console.log(e.target.files);
});
