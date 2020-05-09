const selectedList = document.querySelectorAll(".selected");
const optionsContainer = document.querySelectorAll(".option-container");
const optionsList = document.querySelectorAll(".option");
selectedList.forEach(selected => {
    selected.addEventListener("click", () => {
        selected.parentNode.getElementsByClassName("option-container")[0].classList.toggle("active");
    })
})
optionsList.forEach(option => {
    option.addEventListener("click", () => {
        option.parentNode.parentNode.getElementsByClassName("selected")[0].innerHTML = option.querySelector("label").innerHTML;
        option.parentNode.classList.remove("active");
    })
})
