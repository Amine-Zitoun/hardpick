export function showWin(data) {
    const general = document.getElementsByClassName("general2")[0];
    const winner = document.getElementsByClassName("won")[0];
    const site = document.getElementsByClassName("link")[0];
    const cash = document.getElementsByClassName("cash")[0];
    let differnce = 0;
    let url;
    console.log(data);
    switch (data.site) {
        case "sbs":
            url = "www.sbsinformatique.com";
            break;
        case "mega":
            url = "www.mega-pc.net";
            break;
        case "tunisia":
            url = "www.tunisianet.com.tn";
            break;
        case "extreme":
            url = "extremegaming.tn";
            break;
        case "wiki":
            url = "www.wiki.tn";
            break;
        }
        if (data.pr == "higher") {
            differnce = data.differnce;
            general.innerHTML = `Ufortunately, nothing is available at your budget,</br>but for an extra ${(differnce / 1000)}${data.unit} you can get:`
            if (!(general.classList.value.includes("sorry"))) {
                general.classList.toggle("sorry")
            }
            winner.innerHTML = data.name;
            site.innerHTML = `<a href="${url}">${url}</a>`;
            cash.innerHTML = `${(data.price / 1000)}${data.unit}`
            } else {
                if (general.classList.value.includes("sorry")) {
                    general.classList.toggle("sorry")
                }
                winner.innerHTML = data.name;
                site.innerHTML = `<a href="${url}">${url}</a>`;
                cash.innerHTML = `${(data.price / 1000)}${data.unit}`
            }
}