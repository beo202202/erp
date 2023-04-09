const body = document.querySelector("body");
const MIN_DURATION = 10;

function MakeBlossomFlake() {
    const blossomflake = document.createElement("div");
    const delay = Math.random() * 10;
    const initialOpacity = Math.random();
    const duration = Math.random() * 20 + MIN_DURATION

    blossomflake.classList.add("blossom_flake");
    blossomflake.style.left = `${Math.random() * window.screen.width}px`;
    blossomflake.style.animationDelay = `${delay}s`;
    blossomflake.style.opacity = initialOpacity;
    blossomflake.style.animation = `fall ${duration}s linear`;



    body.appendChild(blossomflake);

    setTimeout(() => {
        body.removeChild(blossomflake);
        MakeBlossomFlake()
    }, (duration + delay) * 1000);
}

MakeBlossomFlake();
for (let index = 0; index < 50; index++) {
    setTimeout(MakeBlossomFlake, 500 * index);
}
