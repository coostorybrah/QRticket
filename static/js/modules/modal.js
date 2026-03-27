import { isAuthLocked } from "./authGuard.js";

export function initModalTriggers() {
    document.addEventListener("click", (e) => {
        // OPEN
        const openBtn = e.target.closest("[data-open]");
        if (openBtn) {
            const modalId = openBtn.dataset.open;

            document.querySelectorAll(".modal").forEach(m => {
                m.classList.remove("active");
            });

            document.getElementById(modalId)?.classList.add("active");
        }

        // CLOSE
        const closeBtn = e.target.closest("[data-close]");
        if (closeBtn) {

            if (isAuthLocked()) {
                window.location.replace("/");
                return;
            }

            const modalId = closeBtn.dataset.close;
            document.getElementById(modalId)?.classList.remove("active");
        }
    });
}