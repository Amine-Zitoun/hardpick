export function doubleScreen(res) {
    if (!(res.classList.value.includes("on"))) {
        res.classList.toggle("on");
        AOS.refreshHard()
    }
}

