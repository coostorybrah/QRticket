import { clearTokens, setTokens } from "./token.js";
import { publicFetch } from "./generalApi.js";
import { unlockAuthUI } from "./authGuard.js";

export function initSignUp(){
    const form = document.getElementById("signUp-form");
    if (!form) return;

    form.addEventListener("submit", async (e)=>{
        e.preventDefault();

        const username = form.username.value.trim();
        const email = form.email.value.trim();
        const password = form.password.value;
        const confirm = form.password_confirm.value;

        if (password !== confirm){
            alert("Mật khẩu không khớp");
            return;
        }

        try {
            const data = await publicFetch("/api/signup/", {
                method: "POST",
                body: JSON.stringify({ username, email, password })
            });

            if (data.success){
                alert(data.message);
                location.reload();
            } else{
                alert(data.message || data.error);
            }

        } catch (err) {
            console.error(err);
            alert("Signup failed");
        }
    });
}

export function initLogin(){
    const form = document.getElementById("login-form");
    if (!form) return;

    form.addEventListener("submit", async (e)=>{
        e.preventDefault();

        const username = form.username.value.trim();
        const password = form.password.value;

        try {
            const data = await publicFetch("/api/login/", {
                method: "POST",
                body: JSON.stringify({ username, password })
            });

            if (data.success){
                setTokens(data);
                unlockAuthUI();
                location.reload();
            } else{
                alert(data.message || data.error);
            }

        } catch (err) {
            console.error(err);
            alert("Login failed");
        }
    });
}

export function logout() {
    clearTokens();
    window.location.href = "/"; // or "/login/"
}