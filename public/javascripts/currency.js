export function updateCurrency(change, option) {
    let currency = document.querySelector(".money")
    const optionLabel = option.childNodes[1].id;
    if (optionLabel == "tn" && change != "Pick an item") {
        document.documentElement.style.setProperty("--pseudo-font", "10px");
        document.documentElement.style.setProperty("--pseudo-height", "3.2");
        switch (change.innerHTML) {
            case "Tunisia":
                currency.setAttribute("money-content", "TND");
                break;
        }
    }
    return;
}