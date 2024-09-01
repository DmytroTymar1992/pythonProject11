document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll(".select").forEach((el) => {
    el.addEventListener("click", function (e) {
      console.log(e);
      if (e.target && e.target.matches(".option")) {
        this.querySelector(".shown").innerHTML = e.target.innerHTML;
      }
      this.classList.toggle("collapsed");
    });
  });

  Select(document.querySelector(".beatu-select"));

  function Select(yourselect) {
    yourselect.style.display = "none";
    let newdiw = document.createElement("div");
    let parentDiv = yourselect.parentNode;
    parentDiv.insertBefore(newdiw, yourselect);
    newdiw.classList.add("selectel");
    newdiw.innerHTML = `<div class="button">${yourselect.dataset.description}</div><div class="selectlist"> </div>`;
    let list = newdiw.querySelector(".selectlist");
    yourselect.querySelectorAll("option").forEach((element) => {
      list.innerHTML += `<div data-id="${element.index}">${element.text}</div>`;
    });
    newdiw.querySelector(".button").onclick = function () {
      if (list.style.display == "block") list.style.display = "none";
      else list.style.display = "block";
    };
    newdiw.querySelectorAll(".selectlist > div").forEach((element) => {
      element.onclick = function () {
        newdiw.querySelectorAll(".selectlist > div").forEach((element) => {
          element.classList.remove("active");
        });
        newdiw.querySelector(".button").innerText = this.innerText;
        this.classList.add("active");
        list.style.display = "none";
        yourselect.options[this.dataset.id].selected = true;
      };
    });
  }

  (function () {
    "use strict";

    const section = document.querySelectorAll(".section");
    const sections = {};
    let i = 0;

    Array.prototype.forEach.call(section, function (e) {
      sections[e.id] = e.offsetTop - 50;
    });

    window.onscroll = function () {
      const scrollPosition =
        document.documentElement.scrollTop || document.body.scrollTop;

      for (let i in sections) {
        if (sections[i] <= scrollPosition) {
          document.querySelector(".active").classList.remove("active");
          document
            .querySelector("a[href*=" + i + "]")
            .classList.add("active");
        }
      }
    };
  })();
});
