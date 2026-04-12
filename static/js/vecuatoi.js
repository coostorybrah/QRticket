import { protectedFetch } from "./modules/generalApi.js";
import { requireAuth } from "./modules/authGuard.js";
import { formatDate, formatTime } from "./modules/format.js";

document.addEventListener("DOMContentLoaded", async () => {
    const allowed = await requireAuth();
    if (!allowed) return;

    loadTickets();
});

async function loadTickets() {
    try {
        const data = await protectedFetch("/api/orders/my-tickets/");
        const container = document.getElementById("tickets");

        if (!data.length) {
            container.innerHTML = "<p>Bạn chưa có vé nào.</p>";
            return;
        }

        const grouped = {};

        data.forEach(ticket => {
            const key = ticket.event_name;

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
            const first = tickets[0];
            return `
            <div class="event-group-container">
                <div class="event-group">
                    <div class="event-info">
                        <h2>${event}</h2>
                        <hr>
                        <p class="event-date-text"> Thời gian: 
                            <span class="event-date">${formatDate(first.date)}</span>
                            <span class="text-separator"> | </span>
                            <span class="event-time">${formatTime(first.start_time)}</span> -
                            <span class="event-time">${formatTime(first.end_time)}</span>
                        </p>

                        <div class="event-venue-info">
                            <p class="event-venue-name venue-info">
                                <span class="event-venue-name-text">Địa điểm:</span>${first.venue_name}
                            </p>
                            <p class="event-venue-address venue-info">
                                <span class="event-venue-address-text">Địa chỉ cụ thể:</span>${first.venue_address} - 
                                <span class="event-venue-city">${first.venue_city}</span>
                            </p>
                        </div>
                    </div>

                    ${tickets.map(ticket => `
                        <hr class="ticket-separator">
                        <div class="ticket-card">
                            <div class="ticket-info">
                                <p class="ticket-type">${ticket.ticket_type}</p>
                            </div>

                            <div class="ticket-image">
                                <img class="qr-code ${ticket.is_used ? 'used' : 'unused'}" src="${ticket.qr_code}">
                                <p class="ticket-status ${ticket.is_used ? 'used' : 'unused'}">
                                    ${ticket.is_used ? "Đã sử dụng" : "Chưa sử dụng"}
                                </p>
                            </div>
                        </div>
                    `).join("")}
                </div>
            </div>

            `;
        }).join("");

    } catch (err) {
        console.error(err);
        document.getElementById("tickets").innerHTML =
            "<p>Lỗi khi tải vé</p>";
    }
}