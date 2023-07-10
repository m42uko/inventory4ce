var btn = document.getElementById("btn");
var icon = document.getElementById("icon");
btn.addEventListener("click", function () {
  icon.classList.add("rotate");
  setTimeout(() => {
    window.location.reload();
  }, 300);
});
