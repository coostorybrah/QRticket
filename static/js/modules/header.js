import { protectedFetch } from "./generalApi.js";
import { clearTokens } from "./token.js";

export async function initHeader() {
    const container = document.getElementById("authContainer");
    if (!container) return;

    try {
        const data = await protectedFetch("/api/auth/me/");

        if (!data.loggedIn) {
            renderGuest(container);
            return;
        }

        renderUser(container, data);

    } catch (err) {
        renderGuest(container);
    }
}

function renderGuest(container) {   
    container.innerHTML = `
        <div id="guestUI" class="wrapper">
            <button type="button" class="modal-trigger" data-open="mdl-login">Đăng nhập</button>
            <span class="text-separator">|</span>
            <button type="button" class="modal-trigger" data-open="mdl-signUp">Đăng ký</button>
        </div>
    `;
}

function renderUser(container, user) {
    container.innerHTML = `
        <a class="eventManager wrapper" href="${window.URLS.myEvents}">Tạo sự kiện</a>
        
        ${user.is_organizer ?
        `<a class="scanner wrapper" href="${window.URLS.scanner}">Quét vé</a>` : 
        `<a class="ticketManager wrapper" href="${window.URLS.myTickets}">Vé của tôi</a>`}

        <div id="userMenu" class="dropdown-hover">
            <a id="userWrapper" href="${window.URLS.userPage}">
                <img id="avatarHeader" src="${user.avatar || '/static/images/avatars/default-avatar.png'}">
                <span id="avatarText">Tài khoản</span>
            </a>

            <div class="dropdown">
                <a href="${window.URLS.myTickets}">Vé của tôi</a>
                <a href="${window.URLS.userPage}">Tài khoản của tôi</a>
                <a id="logoutBtn">Đăng xuất</a>
            </div>
        </div>
    `;

    document.getElementById("logoutBtn")?.addEventListener("click", () => {
        clearTokens();
        location.reload();
    });
}