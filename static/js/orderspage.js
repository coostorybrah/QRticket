import { fetchEvent } from "./orders/api.js";
import { renderTickets, attachTicketEvents, getSelectedItems } from "./orders/tickets.js";
import { updateTotalUI, renderEvent } from "./orders/ui.js";
import { initCheckout } from "./orders/checkout.js";
import { requireAuth } from "./modules/authGuard.js";

document.addEventListener("DOMContentLoaded", async () => {
    const allowed = await requireAuth();
    
    if (!allowed) {
        document.querySelector(".checkout").style.display = "none";
        throw new Error("Not authenticated");
    }
});


const ticketList = document.getElementById("ticketList");
const totalPriceEl = document.getElementById("totalPrice");
const eventNameEl = document.getElementById("eventName");
const eventImageEl = document.getElementById("eventImage");
const payBtn = document.getElementById("payBtn");
const form = document.getElementById("paymentForm");

let total = 0;
let event;
try {
    event = await fetchEvent(event_id);
} catch (err) {
    console.error(err);
    alert("Failed to load event. Please login again.");
    throw err;
}

renderEvent(event, eventNameEl, eventImageEl);
renderTickets(ticketList, event.tickets);

function updateTotal() {
    total = 0;

    document.querySelectorAll(".ticket-row").forEach(row => {
        const price = parseFloat(row.dataset.price);
        const qty = parseInt(row.querySelector(".qty").innerText) || 0;
        total += price * qty;
    });

    updateTotalUI(totalPriceEl, payBtn, total);
}

attachTicketEvents(updateTotal);
initCheckout(form, payBtn, getSelectedItems);

