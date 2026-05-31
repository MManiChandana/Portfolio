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
    introEnter.addEventListener("click", startIntroSequence);
}

window.addEventListener("load", () => {
    if (introOverlay) {
        animateIntroImages();
    }
});

function sleep(ms) {
    return new Promise((res) => setTimeout(res, ms));
}

async function startIntroSequence() {
    const imgs = Array.from(document.querySelectorAll('.intro-image')).map((i) => i.src).filter(Boolean).slice(0,5);
    if (!imgs.length) {
        hideIntroOverlay();
        return;
    }

    // create full-screen viewer
    const viewer = document.createElement('div');
    viewer.className = 'intro-viewer';
    viewer.innerHTML = '<img class="intro-viewer-img" src="" alt="preview">';
    document.body.appendChild(viewer);
    const imgEl = viewer.querySelector('.intro-viewer-img');

    for (let i = 0; i < imgs.length; i++) {
        imgEl.style.opacity = '0';
        imgEl.style.transform = 'scale(1.06)';
        imgEl.src = imgs[i];
        // small delay for image to load
        try {
            await new Promise((resolve, reject) => {
                imgEl.onload = () => resolve();
                imgEl.onerror = () => resolve();
            });
        } catch (e) {}

        // show and animate
        await sleep(60);
        imgEl.style.transition = 'transform 1.8s ease, opacity 0.6s ease';
        imgEl.style.opacity = '1';
        imgEl.style.transform = 'scale(1)';

        // wait for display time (2s)
        await sleep(2000);
    }

    // cleanup viewer and reveal site
    viewer.style.transition = 'opacity 400ms ease';
    viewer.style.opacity = '0';
    await sleep(420);
    viewer.remove();
    hideIntroOverlay();
}
const heroVideo = document.getElementById("heroVideo");
if (heroVideo) {
    const storageKey = "portfolioHeroVideoPlayed";
    const isFirstVisit = localStorage.getItem(storageKey) !== "true";
    const heroObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.target !== heroVideo) {
                    return;
                }
                if (!entry.isIntersecting && !heroVideo.paused) {
                    heroVideo.pause();
                }
            });
        },
        { threshold: 0.25 }
    );

    heroObserver.observe(heroVideo);

    heroVideo.addEventListener("play", () => {
        localStorage.setItem(storageKey, "true");
    });

    if (isFirstVisit) {
        heroVideo.muted = true;
        heroVideo.play().then(() => {
            heroVideo.muted = false;
        }).catch(() => {
            heroVideo.muted = true;
        });
    }

    window.addEventListener("scroll", () => {
        if (!heroVideo || heroVideo.paused) {
            return;
        }
        const rect = heroVideo.getBoundingClientRect();
        if (rect.bottom < 100 || rect.top > window.innerHeight - 100) {
            heroVideo.pause();
        }
    });
}

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
