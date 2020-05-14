const button = document.querySelector(".btn-primary");
const spinner = document.querySelector(".spinner");

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

function apiResponded() {
    fetch("http://localhost:3000/search")
        .then(response => {
            if (response.ok) {
                response.json()
                    .then(data => {
                        if (data) {
                            buttonToSpin();
                        } else {
                            apiResponded();
                        }
                    })
            } else {
                console.log("fetch failure")
            }
        })
}