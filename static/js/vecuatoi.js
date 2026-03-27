import { requireAuth } from "./modules/authGuard.js";

document.addEventListener("DOMContentLoaded", async () => {
    const allowed = await requireAuth();
    
    if (!allowed) {
        document.querySelector(".checkout").style.display = "none";
        throw new Error("Not authenticated");
    }
});