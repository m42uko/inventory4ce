document.addEventListener("DOMContentLoaded", function (event) {
  const linkColor = document.querySelectorAll(".nav_link");

  const current = window.location.pathname;
  linkColor.forEach((l) => {
    var link = l.getAttribute("href");
    if (link == current) {
      l.classList.add("active");
    }
  });

  function colorLink() {
    if (linkColor) {
      linkColor.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");
    }
  }
  linkColor.forEach((l) => l.addEventListener("click", colorLink));
});
