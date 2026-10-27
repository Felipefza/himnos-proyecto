
const toggleMode = () => {
    const darkMode = document.getElementsByTagName("html")[0].dataset.bsTheme

    if (darkMode == "dark") {
        document.getElementsByTagName("html")[0].dataset.bsTheme = "";
        const icon = document.getElementById("toggle-mode-icon");
        icon.classList.toggle("bi-sun")
        icon.classList.toggle("bi-moon")

        localStorage.setItem("darkMode", "null");
    }
    else {
        document.getElementsByTagName("html")[0].dataset.bsTheme = "dark";
        const icon = document.getElementById("toggle-mode-icon");
        icon.classList.toggle("bi-sun")
        icon.classList.toggle("bi-moon")

        localStorage.setItem("darkMode", "dark");
    }
}


addEventListener("DOMContentLoaded", () => {
    const localDarkMode = localStorage.getItem("darkMode");

    if (localDarkMode == "dark") {
        toggleMode();
    }
})
