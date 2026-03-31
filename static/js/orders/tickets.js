import { formatPrice } from "../modules/format.js";

export function renderTickets(ticketList, tickets) {
    let html = "";
    
    tickets.forEach(ticket => {
        html += `
        <div class="ticket-row" 
            data-ticket-id="${ticket.id}" 
            data-price="${ticket.gia}"
            data-available="${ticket.available}">
            
            <div class="ticket-info">${ticket.loai}</div>

            <div class="ticket-price">${formatPrice(ticket.gia)}</div>

            <div class="ticket-controls">
                <button class="minus qty-btn">-</button>
                <input type="number" class="qty-input" value="0" min="0" max="${ticket.available}">
                <button class="plus qty-btn">+</button>
            </div>
        </div>
        `;
    });

    ticketList.innerHTML = html;
}

export function attachTicketEvents(updateTotal) {

    // CLICK → + / -
    document.addEventListener("click", (e) => {

        // PLUS
        if (e.target.classList.contains("plus")) {
            const row = e.target.closest(".ticket-row");
            const input = row.querySelector(".qty-input");

            let qty = parseInt(input.value) || 0;
            const max = parseInt(input.max);

            if (qty < max) {input.value = qty + 1;}


            updateTotal();
        }

        // MINUS
        if (e.target.classList.contains("minus")) {
            const row = e.target.closest(".ticket-row");
            const input = row.querySelector(".qty-input");

            let qty = parseInt(input.value) || 0;
            input.value = Math.max(0, qty - 1);

            updateTotal();
        }
    });

    // INPUT → manual typing
    document.addEventListener("input", (e) => {
        if (e.target.classList.contains("qty-input")) {
            const input = e.target;
            let qty = parseInt(input.value) || 0;

            const max = parseInt(input.max) || Infinity;

            if (qty < 0) {qty = 0;}
            if (qty > max) {qty = max;}

            input.value = qty;

            updateTotal();
        }
    });

    // KEYDOWN → prevent weird values
    document.addEventListener("keydown", (e) => {
        if (e.target.classList.contains("qty-input")) {
            if (e.key === "-" || e.key === "e") {
                e.preventDefault();
            }
        }
    });

    // PASTE → block invalid input
    document.addEventListener("paste", (e) => {
        if (e.target.classList.contains("qty-input")) {
            const pasted = e.clipboardData.getData("text");

            if (!/^\d+$/.test(pasted)) {
                e.preventDefault();
            }
        }
    });
}

export function getSelectedItems() {
    const items = [];

    document.querySelectorAll(".ticket-row").forEach(row => {
        const qty = parseInt(row.querySelector(".qty-input").value) || 0;

        if (qty > 0) {
            items.push({
                ticket_type_id: row.dataset.ticketId, // ✅ THIS MUST EXIST
                quantity: qty
            });
        }
    });

    return items;
}