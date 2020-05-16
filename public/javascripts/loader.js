import {doubleScreen} from './showResult.js';

const button = document.querySelector(".btn-primary");
const spinner = document.querySelector(".spinner");
const res = document.querySelector(".res");

button.addEventListener("click", () => {
    apiResponded();
    setTimeout(() => {
        buttonToSpin();
    }, 200)
})

function buttonToSpin () {
    button.classList.toggle("spin");
    spinner.classList.toggle("active")
}

function end() {
    fetch("http://localhost:3000/search/end")
        .then(response => response.json())
        .then(data => console.log(data))
}

function apiResponded() {
    fetch("http://localhost:3000/search")
        .then(response => {
            if (response.ok) {
                response.json()
                    .then(data => {
                        if (data) {
                            buttonToSpin();
                            end();
                            doubleScreen(res);
                            window.scroll({
                                top :findPos(document.getElementById("res")),
                                behavior: 'smooth'
                            });
                        } else {
                            apiResponded();
                        }
                    })
            } else {
                console.log("fetch failure")
            }
        }).catch(err => console.log(err))
}

function findPos(obj) {
    var curtop = 0;
    if (obj.offsetParent) {
        do {
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
    return curtop;
    }
}