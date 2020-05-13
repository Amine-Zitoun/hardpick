export function updateIcon(change, option) {
    const optionLabel = option.childNodes[1].id;
    if (optionLabel == "gpu" || optionLabel == "cpu" || optionLabel == "ram") {
        switch (change.innerHTML) {
            case "CPU":
                document.documentElement.style.setProperty("--icon-url", "url(../icons/cpu.svg");
                break;
            case "GPU":
                document.documentElement.style.setProperty("--icon-url", "url(../icons/gpu.svg");
                break;
            case "RAM":
                document.documentElement.style.setProperty("--icon-url", "url(../icons/ram.svg)");
                break;
        }        
    }
    return;
}