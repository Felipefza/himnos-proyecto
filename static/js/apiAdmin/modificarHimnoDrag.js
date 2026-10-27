
class parrafo {

    constructor(id, ul) {
        this.id = id;
        this.ul = ul;
        this.innerHTML = null;
    }

    getInnerHTML(optionSelectedValue) {
        if (this.innerHTML !== null) {
            return;
        }

        let firstOptionSelected;
        let firstOptionValue;

        let secondOptionSelected;
        let secondOptionValue;

        if (optionSelectedValue === "parrafo") {
            firstOptionSelected = "Parrafo";
            firstOptionValue = "parrafo";

            secondOptionSelected = "Coro";
            secondOptionValue = "coro";
        } else if (optionSelectedValue === "coro") {
            firstOptionSelected = "Coro";
            firstOptionValue = "coro";

            secondOptionSelected = "Parrafo";
            secondOptionValue = "parrafo";
        } else {
            firstOptionSelected = "Parrafo";
            firstOptionValue = "parrafo";

            secondOptionSelected = "Coro";
            secondOptionValue = "coro";
        }

        this.innerHTML =
        `<li class="list-group-item bg-light shadow card d-flex flex-row align-items-center mb-5 mt-5 fs-4 draggable-list" data-id="${ this.id }">
            <div class="d-flex flex-row align-items-center w-100 bg-light" draggable="true">
                <span>
                    <i class="bi bi-grip-horizontal" style="font-size: 3rem;"></i>
                </span>
                <div class="container m-3">
                    <select class="form-select mb-2 w-auto" name="opcionParrafo">
                        <option value="${ firstOptionValue }" selected>${ firstOptionSelected }</option>
                        <option value="${ secondOptionValue }">${ secondOptionSelected }</option>
                    </select>
                    <textarea class="form-control" rows="8" placeholder="Ingrese el Parrafo..." name="textoParrafo" required></textarea>
                </div>
            </div>
            <button type="button" class="btn" onClick="removeParrafo(${ this.id })">
                <i class="bi bi-trash-fill" style="font-size: 2rem;"></i>
            </button>
        </li>`
    }

    insertInnerHTML() {
        if (this.innerHTML === null) {
            return;
        }

        this.ul.insertAdjacentHTML("beforeend", this.innerHTML);
    }

}

const listUl = document.getElementById("list-ul");

let indexParrafos = 0

let draggedId = null;

function startListeners() {
    const dragablesLista = document.querySelectorAll(".draggable-list");

    dragablesLista.forEach(item => {
        item.addEventListener("dragstart", (event) => {
            const row = event.target.closest(".draggable-list");
            if (!row) {
                return;
            }
            draggedId = Number(row.dataset.id);

            row.classList.add("opacity-25");
            event.dataTransfer.effectAllowed = "move";
        });

        item.addEventListener("dragend", () => {
            document.querySelectorAll(".draggable-list").forEach(targetRow => {
                targetRow.classList.remove("opacity-25");
                targetRow.classList.remove("border-primary");
            })
            draggedId = null;
        })

        item.addEventListener("dragover", (event) => {
            event.preventDefault();
            const row = event.target.closest(".draggable-list");

            document.querySelectorAll(".draggable-list").forEach(targetRow => {
                targetRow.classList.remove("border-primary");
            });

            if (row && Number(row.dataset.id) !== draggedId) {
                row.classList.add("border-primary");
            }
        });

        item.addEventListener("drop", (event) => {
            event.preventDefault();
            const targetRow = event.target.closest(".draggable-list");
            if (!targetRow || draggedId === null) {
                return;
            }
            const targetId = Number(targetRow.dataset.id);
            if (targetId === draggedId) {
                return;
            }

            const rows = document.querySelectorAll(".draggable-list")

            for (row of rows) {
                if (Number(row.dataset.id) === draggedId) {
                    listUl.insertBefore(row, targetRow.nextSibling);
                }
            }
        });

        //item.addEventListener("dragenter", (event) => {});

        //item.addEventListener("dragleave", (event) => {});
    })
}

function addParrafo(typeParrafo) {
    if (parrafo === undefined) {
        typeParrafo = "parrafo"
    }

    const nuevoParrafo = new parrafo(indexParrafos, listUl);
    nuevoParrafo.getInnerHTML(typeParrafo);
    nuevoParrafo.insertInnerHTML();
    indexParrafos += 1;
    startListeners();
}

function removeParrafo(dataIndex) {
    const draggableLista = document.querySelectorAll(".draggable-list")
    draggableLista.forEach(item => {
        if (Number(item.dataset.id) === Number(dataIndex)) {
            listUl.removeChild(item);
        }
    })
}

startListeners();
