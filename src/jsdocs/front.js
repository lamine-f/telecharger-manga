const firstInput = document.getElementById("first");
const lastInput = document.getElementById("last");

// Ajoute un écouteur d'événement à l'input "last" pour vérifier sa valeur à chaque changement
lastInput.addEventListener("input", () => {
const firstValue = parseInt(firstInput.value);
const lastValue = parseInt(lastInput.value);

// Vérifie si la valeur de l'input "last" est inférieure à celle de l'input "first"
if (lastValue < firstValue) {
    lastInput.value = firstValue;
}
});

// Ajoute un écouteur d'événement à l'input "first" pour vérifier sa valeur à chaque changement
firstInput.addEventListener("input", () => {
    const firstValue = parseInt(firstInput.value);
    const lastValue = parseInt(lastInput.value);

    // Vérifie si la valeur de l'input "first" est supérieure à celle de l'input "last"
    if (firstValue > lastValue) {
    firstInput.value = lastValue;
    }else if (firstValue <= 1){
        firstInput.value = 1
    }
    });