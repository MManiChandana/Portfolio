const modal = document.querySelector("#infoModal");

function openModal({ title, desc, tech, image, live, repo, liveLabel, imageMode, logos }) {
    if (!modal) {
        return;
    }

    modal.classList.add("is-open");
    modal.classList.toggle("is-image-view", imageMode === "full");
    modal.setAttribute("aria-hidden", "false");
    modal.querySelector("h2").textContent = title || "";
    const logosContainer = modal.querySelector('.modal-logos');
    if (logosContainer) {
        logosContainer.innerHTML = '';
        try {
            if (Array.isArray(logos)) {
                logos.forEach((src) => {
                    const img = document.createElement('img');
                    img.src = src;
                    img.alt = title + ' logo';
                    logosContainer.appendChild(img);
                });
            }
        } catch (e) {
            logosContainer.innerHTML = '';
        }
    }
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
        liveLink.textContent = liveLabel || "Open Live Project";
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
    modal.classList.remove("is-image-view");
    modal.setAttribute("aria-hidden", "true");
}

document.querySelectorAll(".skill-card").forEach((card) => {
    card.addEventListener("click", () => {
        let logos = [];
        try {
            if (card.dataset.logos) logos = JSON.parse(card.dataset.logos);
        } catch (e) { logos = []; }
        openModal({
            title: card.dataset.title,
            desc: card.dataset.desc,
            tech: "Skill",
            image: "",
            live: "",
            repo: "",
            logos: logos,
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

document.querySelectorAll(".cert-detail").forEach((button) => {
    button.addEventListener("click", () => {
        openModal({
            title: button.dataset.title,
            desc: button.dataset.desc,
            tech: button.dataset.tech,
            image: button.dataset.image,
            live: button.dataset.link,
            repo: "",
            liveLabel: "Open Certificate",
            imageMode: "full",
        });
    });
});

document.querySelectorAll(".virtual-project-detail").forEach((button) => {
    button.addEventListener("click", () => {
        openModal({
            title: button.dataset.title,
            desc: button.dataset.desc,
            tech: button.dataset.tech,
            image: button.dataset.image,
            live: button.dataset.link,
            repo: "",
            liveLabel: "Open Experience",
            imageMode: "full",
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

const introOverlay = document.getElementById("siteIntro");
const introEnter = document.getElementById("introEnter");
const introImages = document.querySelectorAll(".intro-image-wrapper");

function animateIntroImages() {
    introImages.forEach((wrapper, index) => {
        window.setTimeout(() => {
            wrapper.classList.add("is-visible");
        }, index * 700);
    });

    if (introEnter) {
        window.setTimeout(() => {
            introEnter.classList.add("visible");
        }, introImages.length * 700);
    }
}

function hideIntroOverlay() {
    if (!introOverlay) {
        return;
    }
    introOverlay.classList.add("is-hidden");
    window.setTimeout(() => {
        introOverlay.remove();
    }, 600);
}

if (introEnter) {
    introEnter.addEventListener("click", hideIntroOverlay);
}

window.addEventListener("load", () => {
    if (introOverlay) {
        animateIntroImages();
    }
});

function animateDashboardCounters() {
    document.querySelectorAll(".dashboard-value").forEach((element) => {
        const endValue = Number(element.dataset.value) || 0;
        const duration = 700;
        const stepTime = Math.max(Math.floor(duration / Math.max(endValue, 1)), 20);
        let current = 0;
        const timer = setInterval(() => {
            current += 1;
            element.textContent = current;
            if (current >= endValue) {
                clearInterval(timer);
            }
        }, stepTime);
    });
}

animateDashboardCounters();

/* Hero audio autoplay and scroll-to-play handling */
const heroAudio = document.getElementById("heroAudio");
const unmuteBtn = document.getElementById("unmuteBtn");
const audioPlayedKey = "portfolioHeroAudioPlayed";
if (heroAudio) {
    const tryPlayAudio = () => {
        if (!heroAudio) return Promise.reject();
        return heroAudio.play().then(() => {
            try { localStorage.setItem(audioPlayedKey, "true"); } catch (e) {}
            if (unmuteBtn) unmuteBtn.classList.remove("visible");
        });
    };

    const audioObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const already = localStorage.getItem(audioPlayedKey) === "true";
                if (!already) {
                    tryPlayAudio().catch(() => {
                        if (unmuteBtn) unmuteBtn.classList.add("visible");
                    });
                }
            }
        });
    }, { threshold: 0.5 });

    const heroSection = document.querySelector('.hero');
    if (heroSection) audioObserver.observe(heroSection);

    if (unmuteBtn) {
        unmuteBtn.addEventListener('click', () => {
            tryPlayAudio().catch(() => {});
        });
    }
}

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
