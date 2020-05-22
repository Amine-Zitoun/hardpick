import {doubleScreen} from './showResult.js';
import {checkErr, noErr} from './inputValidation.js';
import {showWin} from './fillWinner.js';

const button = document.querySelector(".btn-primary");
const spinner = document.querySelector(".spinner");
const res = document.querySelector(".res");
const errContainer = document.getElementsByClassName("error-message")[0];

function buttonToSpin () {
    button.classList.toggle("spin");
    spinner.classList.toggle("active")
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

function masterFunc() {
    let valid = checkErr(errContainer);
    if (valid) {
        noErr(errContainer)
        buttonToSpin();
        let comp = document.getElementById("comp").innerHTML.toLowerCase();
        let region = document.getElementById("region").innerHTML.toLowerCase();
        let price = +(document.getElementById("price").value);
        fetch("https://hardpick.herokuapp.com/search", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                comp: comp,
                region: region,
                price: price
            })
        }).then(data => {
            return data.json()
        }).then(resp => {
            buttonToSpin();
            showWin(resp);
            doubleScreen(res);
            window.scroll({
                top :findPos(document.getElementById("res")),
                behavior: 'smooth'
            });
        }).catch(err => {
            console.log(err);
        })
    }
}


button.addEventListener("click", () => {
    masterFunc();
})