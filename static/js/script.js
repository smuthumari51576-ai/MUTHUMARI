document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".btn-custom");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            button.classList.add("btn-click");

            setTimeout(() => {
                button.classList.remove("btn-click");
            }, 150);
        });
    });
});
