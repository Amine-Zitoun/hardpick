function checkErr(errContainer) {
    let error;
    let region = document.getElementById("region").innerHTML.toLocaleLowerCase();
    let budget = document.getElementById("price").value;
    let unit;
    let correct = true;
    switch (region) {
        case "tunisia":
            unit = "TND";
            break;
    }
    if (region == "pick an item" && !(budget)) {
        correct = false;
        error = "Please enter your country and budget";
        errContainer.innerHTML = error;
        if (errContainer.classList.value == "error-message") {
            errContainer.classList.toggle("on")
        }
    } else if (!(budget)) {
        correct = false;
        error = "Please enter your budget";
        errContainer.innerHTML = error;
        if (errContainer.classList.value == "error-message") {
            errContainer.classList.toggle("on")
        }
    } else if (budget < 30) {
        correct = false;
        error = `Budget too low under 30${unit}`;
        errContainer.innerHTML = error;
        if (errContainer.classList.value == "error-message") {
            errContainer.classList.toggle("on")
        }
    } else if (region == "pick an item") {
        correct = false;
        error = "Plase select your country";
        errContainer.innerHTML = error;
        if (errContainer.classList.value == "error-message") {
            errContainer.classList.toggle("on")
        }
    }
    return correct;
}

function noErr(errContainer) {
    if (errContainer.classList.value.includes("on")) {
        errContainer.classList.toggle("on");
        errContainer.innerHTML = "";
    }
}

export {checkErr, noErr};