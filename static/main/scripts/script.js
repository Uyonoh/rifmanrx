const sidebar = document.querySelector("nav.sidebar");
const sideHandle = document.querySelector("#side-toggle");

sideHandle.addEventListener("click", (e) => {
    sidebar.classList.toggle("hidden");
});

const closeSideHandle = document.querySelector("span.close");

closeSideHandle.addEventListener("click", (e) => {
    sidebar.classList.toggle("hidden");
});