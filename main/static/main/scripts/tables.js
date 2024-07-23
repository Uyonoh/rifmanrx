
// const viewHandlers = document.querySelectorAll(viewSelector);

// function setView(element) {
//     const id = element.getAttribute("id");

//     window.open("/drugs/view/" + id, target="");
// }

// viewHandlers.forEach((element) => {
//     element.addEventListener("click", (e) => {
//         setView(element);
//     });
// });



function setView() {
    const bigViewSelector = "tr.drug"
    const smallViewSelector = "button.view-drug"
    if (window.innerWidth >= 1000) {
        var viewSelector = bigViewSelector;
        const mobileHandles = document.querySelectorAll("td.mobile-only");

        mobileHandles.forEach((div) => {
            div.classList.add("hidden");
        });
        
    } else {
        var viewSelector = smallViewSelector;
        const mobileHandles = document.querySelectorAll("td.mobile-only");

        const bigViewHandles = document.querySelectorAll(bigViewSelector)
        bigViewHandles.forEach((handle) => {
            handle.removeEventListener("click", this);
        })

        mobileHandles.forEach((div) => {
            div.classList.remove("hidden");
        });

    }
    var viewHandlers = document.querySelectorAll(viewSelector);

    viewHandlers.forEach((element) => {
        element.addEventListener("click", function clicked (e) {
            const id = element.getAttribute("id");
            window.open("/drugs/view/" + id, target="_self");
        });
    });
}

window.onload = setView;

window.onresize = setView;