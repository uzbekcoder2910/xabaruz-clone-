document.addEventListener("DOMContentLoaded", function() {
  let list = document.querySelector("#latest-news");
  let items = list.querySelectorAll("li");
  let visibleCount = 5; // show 5 items at once
  let index = 0;

  // Hide all except first 5
  items.forEach((item, i) => {
    if (i >= visibleCount) item.style.display = "none";
  });

  setInterval(() => {
    // hide first item
    items[index].style.display = "none";
    // show next hidden item
    let nextIndex = (index + visibleCount) % items.length;
    items[nextIndex].style.display = "block";

    index = (index + 1) % items.length;
  }, 3000); // change every 3 sec
});
