let interval;

function startRotation() {
    if (!interval) {
        interval = setInterval(_rotateImages, 1000);
    }
}

function _rotateImages() {
    const images = document.getElementsByClassName("ep-plant-image");
    const current_image = document.querySelector(".ep-plant-image.displayed");

    let nextIdx = Array.from(images).indexOf(current_image) + 1;
    if (nextIdx == images.length) {
        nextIdx = 0;
    }

    current_image.classList.add("hidden");
    current_image.classList.remove("displayed");

    images[nextIdx].classList.add("displayed");
    images[nextIdx].classList.remove("hidden");
}


function stopRotation() {
    clearInterval(interval);
    interval = null;
}

document.addEventListener('DOMContentLoaded', function() {
    // Initialisiere Flatpickr für Datumsfelder
    flatpickr(".dateinput, input[type='date']", {
        dateFormat: "d.m.Y",
        locale: "de",
        allowInput: true
    });

    // Initialisiere Flatpickr für Datum/Zeit-Felder
    flatpickr(".datetimeinput", {
        enableTime: true,
        dateFormat: "d.m.Y H:i",
        time_24hr: true,
        locale: "de",
        allowInput: true
    });
});
