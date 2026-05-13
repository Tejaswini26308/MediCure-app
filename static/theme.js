function toggleTheme() {
    document.body.classList.toggle("light-mode");

    const btn = document.getElementById("theme-btn");

    if(document.body.classList.contains("light-mode")){
        localStorage.setItem("theme", "light");

        if(btn){
            btn.innerHTML = "☀️";
        }
    }
    else{
        localStorage.setItem("theme", "dark");

        if(btn){
            btn.innerHTML = "🌙";
        }
    }
}

window.onload = function () {
    const savedTheme = localStorage.getItem("theme");

    if(savedTheme === "light"){
        document.body.classList.add("light-mode");

        const btn = document.getElementById("theme-btn");

        if(btn){
            btn.innerHTML = "☀️";
        }
    }
}