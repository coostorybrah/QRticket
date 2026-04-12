import { protectedFetch } from "./generalApi.js";

let authLocked = false;

export async function requireAuth() {
    try {
        const data = await protectedFetch("/api/auth/me/");

        if (!data.loggedIn) {
            lockAuthUI();
            return false;
        }

        unlockAuthUI();
        return true;

    } catch {
        lockAuthUI();
        return false;
    }
}

export function lockAuthUI() {
    if (authLocked) {
        return;
    }

    authLocked = true;

    openModal("mdl-login"); // default entry
}

export function unlockAuthUI() {
    authLocked = false;

    document.querySelectorAll(".modal").forEach(m => {
        m.classList.remove("active");
    });
}

export function isAuthLocked() {
    return authLocked;
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.warn("Modal not found:", modalId);
        return;
    }

    document.querySelectorAll(".modal").forEach(m => {
        m.classList.remove("active");
    });

    modal.classList.add("active");
}
