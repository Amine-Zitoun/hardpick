import {updateCurrency} from './currency.js';
import {updateIcon} from './update-icon.js';
const selectedList = document.querySelectorAll(".selected");
const optionsContainer = document.querySelectorAll(".option-container");
const optionsList = document.querySelectorAll(".option");

selectedList[0].innerHTML = selectedList[0].parentNode.children[0].getElementsByClassName("option")[0].getElementsByTagName("label")[0].innerHTML;

selectedList.forEach(selected => {
    selected.addEventListener("click", () => {
        selected.parentNode.getElementsByClassName("option-container")[0].classList.toggle("active");
    })
})

optionsList.forEach(option => {
    const selectText = option.parentNode.parentNode.getElementsByClassName("selected")[0];
    option.addEventListener("click", () => {
        selectText.innerHTML = option.querySelector("label").innerHTML;
        option.parentNode.classList.remove("active");
        updateCurrency(selectText, option);
        updateIcon(selectText, option);
    })
})
