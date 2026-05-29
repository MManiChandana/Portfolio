const modal = document.querySelector("#infoModal");

function openModal({ title, desc, tech, image, live, repo }) {
    if (!modal) {
        return;
    }

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    modal.querySelector("h2").textContent = title || "";
    modal.querySelector(".modal-desc").textContent = desc || "";
    modal.querySelector(".modal-tech").textContent = tech || "";

    const modalImage = modal.querySelector(".modal-image");
    modalImage.src = image || "";
    modalImage.alt = title || "";

    const links = modal.querySelector(".modal-links");
    links.innerHTML = "";

    if (live && live !== "#") {
        const liveLink = document.createElement("a");
        liveLink.href = live;
        liveLink.target = "_blank";
        liveLink.rel = "noreferrer";
        liveLink.textContent = "Open Live Project";
        links.appendChild(liveLink);
    }

    if (repo && repo !== "#") {
        const repoLink = document.createElement("a");
        repoLink.href = repo;
        repoLink.target = "_blank";
        repoLink.rel = "noreferrer";
        repoLink.textContent = "Open Repository";
        links.appendChild(repoLink);
    }
}

function closeModal() {
    if (!modal) {
        return;
    }

    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
}

document.querySelectorAll(".skill-card").forEach((card) => {
    card.addEventListener("click", () => {
        openModal({
            title: card.dataset.title,
            desc: card.dataset.desc,
            tech: "Skill",
            image: "",
            live: "",
            repo: "",
        });
    });
});

document.querySelectorAll(".project-detail").forEach((button) => {
    button.addEventListener("click", () => {
        openModal({
            title: button.dataset.title,
            desc: button.dataset.desc,
            tech: button.dataset.tech,
            image: button.dataset.image,
            live: button.dataset.live,
            repo: button.dataset.repo,
        });
    });
});

if (modal) {
    modal.querySelector(".modal-close").addEventListener("click", closeModal);
    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });
}

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeModal();
    }
});

const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
            }
        });
    },
    { threshold: 0.16 }
);

document.querySelectorAll(".reveal").forEach((item) => observer.observe(item));
