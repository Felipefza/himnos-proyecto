const fontSizes = {
    1: "fs-1",
    2: "fs-2",
    3: "fs-3",
    4: "fs-4",
    5: "fs-5",
    6: "fs-6",
}

const listaParrafos = [];

const adjuntarTextoQuery = (listaTextoQuery) => {
    listaTextoQuery.forEach(textoQuerySelector => {
        const parrafos = document.querySelectorAll(textoQuerySelector);
        parrafos.forEach(item => {
            listaParrafos.push(item)
        })
    })
}

const aumentarFontSize = (blockChange) => {
    let canReplace = true;

    const replaceList = new Map();

    listaParrafos.forEach(item => {
        for (let index = 1; index < 7; index++) {
            if (item.classList.contains(fontSizes[index]) && index > 2) {
                replaceList.set(item, index);
            }
            else if (item.classList.contains(fontSizes[index]) && index === 2) {
                replaceList.set(item, index);
                const boton = document.getElementById("aumentar-font-size");
                boton.disabled = true;
            }
            else if (item.classList.contains(fontSizes[index]) && index === 1) {
                canReplace = false;
            }
        }
    })

     if (canReplace) {
         for (let [item, index] of replaceList) {
            item.classList.replace(fontSizes[index], fontSizes[index - 1])
        }

        const fontSize = localStorage.getItem("fontSize");
        if (fontSize !== "null" && blockChange == undefined) {
            localStorage.setItem("fontSize", parseInt(fontSize) + 1);
        }

        const boton = document.getElementById("disminuir-font-size");
        if (boton.disabled) {
            boton.disabled = false;
        }

    }
}

const disminuirFontSize = (blockChange) => {
    let canReplace = true;
    const replaceList = new Map();

    listaParrafos.forEach(item => {
        for (let index = 1; index < 7; index++) {
            if (item.classList.contains(fontSizes[index]) && index < 5) {
                replaceList.set(item, index);
            }
            else if (item.classList.contains(fontSizes[index]) && index === 5) {
                replaceList.set(item, index);
                const boton = document.getElementById("disminuir-font-size");
                boton.disabled = true;
            }
            else if (item.classList.contains(fontSizes[index]) && index === 6) {
                canReplace = false;
            }
        }
    })

    if (canReplace) {
        for (let [item, index] of replaceList) {
            item.classList.replace(fontSizes[index], fontSizes[index + 1])
        }

        const fontSize = localStorage.getItem("fontSize");
        if (fontSize !== "null" && blockChange == undefined) {
            localStorage.setItem("fontSize", parseInt(fontSize) - 1);
        }

        const boton = document.getElementById("aumentar-font-size");

        if (boton.disabled) {
            boton.disabled = false;
        }
    }
}

addEventListener("DOMContentLoaded", () => {
    const primaryFontSize = localStorage.getItem("fontSize");

    if (primaryFontSize !== "null") {
        const cantidadFontSize = parseInt(primaryFontSize);

        if (cantidadFontSize > 0) {
            for (let index = 0; index < cantidadFontSize; index++) {
                aumentarFontSize(true);
            }
        } else if (primaryFontSize < 0) {
            for (let index = 0; index > cantidadFontSize; index--) {
                disminuirFontSize(true);
            }
        }
    }

    else {
        localStorage.setItem("fontSize", 0)
    }
})
