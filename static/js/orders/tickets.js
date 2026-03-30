import { formatPrice } from "../modules/formatPrice.js";

export function renderTickets(ticketList, tickets) {
    let html = "";
    
    tickets.forEach(ticket => {
        html += `
        <div class="ticket-row" 
            data-ticket-id="${ticket.id}" 
            data-price="${ticket.gia}">
            
            <div class="ticket-info">
                <span>${ticket.loai}</span>
                <span>${formatPrice(ticket.gia)}</span>
            </div>

            <div class="ticket-controls">
                <button class="minus quantity-input">-</button>
                <span class="qty">0</span>
                <button class="plus quantity-input">+</button>
            </div>
        </div>
        `;
    });

    ticketList.innerHTML = html;
}

export function attachTicketEvents(updateTotal) {
    document.addEventListener("click", (e) => {

        // PLUS
        if (e.target.classList.contains("plus")) {
            const row = e.target.closest(".ticket-row");
            const qtyEl = row.querySelector(".qty");

            let qty = parseInt(qtyEl.innerText) || 0;
            qty++;

            qtyEl.innerText = qty;
            updateTotal();
        }

        // MINUS
        if (e.target.classList.contains("minus")) {
            const row = e.target.closest(".ticket-row");
            const qtyEl = row.querySelector(".qty");

            let qty = parseInt(qtyEl.innerText) || 0;
            qty = Math.max(0, qty - 1);

            qtyEl.innerText = qty;
            updateTotal();
        }
    });
}

export function getSelectedItems() {
    const items = [];

    document.querySelectorAll(".ticket-row").forEach(row => {
        const qty = parseInt(row.querySelector(".qty").innerText) || 0;

        if (qty > 0) {
            items.push({
                ticket_type_id: row.dataset.ticketId, // ✅ THIS MUST EXIST
                quantity: qty
            });
        }
    });

    return items;
}