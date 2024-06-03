document.querySelectorAll(".select").forEach((el) => {
  el.addEventListener("click", function (e) {
    console.log(e);
    if (e.target && e.target.matches(".option")) {
      this.querySelector(".shown").innerHTML = e.target.innerHTML;
    }
    this.classList.toggle("collapsed");
  });
});
