// Get the modal
const modal = document.getElementById("myModal");

// Get the button that opens the modal
const btn = document.querySelector(".search__link");

// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function () {
  modal.style.display = "flex";
  window.document.body.classList.toggle("no-scroll");
};

// When the user clicks on img (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
  window.document.body.classList.toggle("no-scroll");
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target === modal) {
    modal.style.display = "none";
    window.document.body.classList.toggle("no-scroll");
  }
};

// modal-toggle

const loginSearcher = document.querySelector(".login-searcher");
const loginEmployer = document.querySelector(".login-employer");
const searchBtn = document.querySelector("#searchBtn");
const employerBtn = document.querySelector("#employerBtn");
const modalActions = document.querySelector(".modal-actions");

(function () {
  if (searchBtn.classList.contains("user__actions-modal-active")) {
    loginEmployer.style.display = "none";
    loginSearcher.style.display = "block";
  }
  if (employerBtn.classList.contains("user__actions-modal-active")) {
    loginEmployer.style.display = "block";
    loginSearcher.style.display = "none";
  }
})();

modalActions.addEventListener("click", (e) => {
  e.stopPropagation();
  if (
    e.target.innerHTML === "Пошукачу" &&
    e.target.classList.contains("user__actions-modal-active")
  ) {
    loginEmployer.style.display = "none";
    loginSearcher.style.display = "block";
    employerBtn.classList.remove("user__actions-modal-active");
  } else if (
    e.target.innerHTML === "Пошукачу" &&
    !e.target.classList.contains("user__actions-modal-active")
  ) {
    e.target.classList.add("user__actions-modal-active");
    loginEmployer.style.display = "none";
    loginSearcher.style.display = "block";
    employerBtn.classList.remove("user__actions-modal-active");
  } else if (e.target.innerHTML === "Роботодавцю") {
    e.target.classList.add("user__actions-modal-active");
    loginEmployer.style.display = "block";
    loginSearcher.style.display = "none";
    searchBtn.classList.remove("user__actions-modal-active");
  }
});

// select

// document.querySelectorAll(".select").forEach((el) => {
//   el.addEventListener("click", function (e) {
//     console.log(e);
//     if (e.target && e.target.matches(".option")) {
//       this.querySelector(".shown").innerHTML = e.target.innerHTML;
//     }
//     this.classList.toggle("collapsed");
//   });
// });



