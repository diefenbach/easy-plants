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