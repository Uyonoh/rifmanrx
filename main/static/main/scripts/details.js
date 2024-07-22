const pk = document.querySelector(".drug").id

const sellButton = document.querySelector("button.sell");
const restockButton = document.querySelector("button.restock");
const editButton = document.querySelector("button.edit");

function toSale() {
    const url = "/drugs/sell/" + pk ;
    window.location = (url);
}

function toRestock() {
    const url = "/drugs/restock/" + pk ;
    window.location = (url);
}

function toEdit() {
    const url = "/drugs/edit/" + pk ;
    window.location = (url);
}

sellButton.addEventListener("click", toSale);