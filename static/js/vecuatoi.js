import { apiFetch } from "./modules/generalApi.js";
import { requireAuth } from "./modules/authGuard.js";

document.addEventListener("DOMContentLoaded", async () => {
    const allowed = await requireAuth();
    if (!allowed) return;

    loadTickets();
});

async function loadTickets() {
    try {
        const data = await apiFetch("/api/orders/my-tickets/");
        const container = document.getElementById("tickets");

        if (!data.length) {
            container.innerHTML = "<p>Bạn chưa có vé nào.</p>";
            return;
        }

        const grouped = {};

        data.forEach(ticket => {
            const key = ticket.event;

            if (!grouped[key]) {
                grouped[key] = [];
            }

            grouped[key].push(ticket);
        });

        // SORT events by date
        const sortedEvents = Object.entries(grouped).sort((a, b) => {
            return new Date(a[1][0].date || 0) - new Date(b[1][0].date || 0);
        });

        container.innerHTML = sortedEvents.map(([event, tickets]) => {
            return `
                <div class="event-group">
                    <h2>${event}</h2>
                    ${tickets.map(ticket => `
                        <div class="ticket-card">
                            <p>${ticket.ticket_type}</p>
                            <p>${ticket.date || ""}</p>
                            <img src="${ticket.qr_code}">
                            <p class="${ticket.is_used ? 'used' : 'unused'}">
                                ${ticket.is_used ? "Đã sử dụng" : "Chưa sử dụng"}
                            </p>
                        </div>
                    `).join("")}
                </div>
            `;
        }).join("");

    } catch (err) {
        console.error(err);
        document.getElementById("tickets").innerHTML =
            "<p>Lỗi khi tải vé</p>";
    }
}