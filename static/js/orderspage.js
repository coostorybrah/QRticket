import { fetchEvent, createOrder, addItems, getPaymentUrl } from "./orders/api.js";
import { renderTickets, attachTicketEvents, getSelectedItems } from "./orders/tickets.js";
import { updateTotalUI, renderEvent } from "./orders/ui.js";
import { initCheckout } from "./orders/checkout.js";
import { requireAuth } from "./modules/authGuard.js";


// OPEN LOGIN/SIGN UP MODAL FOR GUEST USER
document.addEventListener("DOMContentLoaded", async () => {
    const allowed = await requireAuth();

    if (!allowed) {
        document.querySelector(".checkout").style.display = "none";
        throw new Error("Not authenticated");
    }
});


// ELEMENTS FOR PAGE RENDERING
const ticketList = document.getElementById("ticketList");
const totalPriceEl = document.getElementById("totalPrice");
const eventNameEl = document.getElementById("eventName");
const eventImageEl = document.getElementById("eventImage");

const payBtn = document.getElementById("payBtn");
const form = document.getElementById("paymentForm");

// payment UI
const cardBtn = document.getElementById("cardOptionBtn");
const paypalTab = document.getElementById("payPalOptionBtn");

const cardSection = document.getElementById("cardSection");
const paypalSection = document.getElementById("paypalSection");
const paypalBtn = document.getElementById("paypalBtn");


// STATE
let paymentMethod = "card";    // Default payment method

let total = 0;
let event;

// LOAD EVENT
try {
    event = await fetchEvent(event_id);
} catch (err) {
    console.error(err);
    alert("Failed to load event. Please login again.");
    throw err;
}

renderEvent(event, eventNameEl, eventImageEl);
renderTickets(ticketList, event.tickets);


// TOTAL CALCULATION
function updateTotal() {
    total = 0;

    document.querySelectorAll(".ticket-row").forEach(row => {
        const price = parseFloat(row.dataset.price);
        const qty = parseInt(row.querySelector(".qty").innerText) || 0;
        total += price * qty;
    });

    updateTotalUI(totalPriceEl, payBtn, total);

    // 🔥 FINAL CONTROL
    if (paymentMethod === "paypal") {
        payBtn.disabled = true;
    } else {
        payBtn.disabled = total === 0;
    }
}

attachTicketEvents(updateTotal);


// CARD METHOD SWITCH
cardBtn.onclick = () => {
    paymentMethod = "card";

    cardSection.style.display = "block";
    paypalSection.style.display = "none";

    payBtn.disabled = total === 0;

    cardBtn.classList.add("active");
    paypalTab.classList.remove("active");

    // Enable validation
    form.noValidate = false;
};

// PAYPAL METHOD SWITCH
paypalTab.onclick = () => {
    paymentMethod = "paypal";

    cardSection.style.display = "none";
    paypalSection.style.display = "block";

    payBtn.disabled = true;

    paypalTab.classList.add("active");
    cardBtn.classList.remove("active");

    // Disable form validation
    form.noValidate = true;
};


// CHECKOUT (CARD FLOW)
initCheckout(
    form,
    payBtn,
    getSelectedItems,
    () => paymentMethod
);


// PAYPAL FLOW
paypalBtn.addEventListener("click", async () => {
    if (paypalBtn.disabled) {
        return;
    }

    paypalBtn.disabled = true;
    paypalBtn.innerText = "Đang xử lý...";
    
    try {
        const items = getSelectedItems();

        if (items.length === 0) {
            alert("Vui lòng chọn ít nhất 1 vé");
            paypalBtn.disabled = false;
            paypalBtn.innerText = "PayPal";
            return;
        }

        const buyerName = document.getElementById("buyerName")?.value;
        const buyerEmail = document.getElementById("buyerEmail")?.value;
        const buyerPhone = document.getElementById("buyerPhone")?.value;

        if (!buyerName || !buyerEmail || !buyerPhone) {
            alert("Vui lòng nhập đầy đủ thông tin");
            paypalBtn.disabled = false;
            paypalBtn.innerText = "PayPal";

            return;
        }

        // create order
        const data = await createOrder({
            buyer_name: buyerName,
            buyer_email: buyerEmail,
            buyer_phone: buyerPhone
        });

        const orderId = data.order_id;

        // add items
        await addItems(orderId, items);

        // get PayPal URL
        const paymentData = await getPaymentUrl(orderId);

        if (!paymentData?.payment_url) {
            throw new Error("Invalid payment URL");
        }

        // redirect to PayPal
        window.location.href = paymentData.payment_url;

    } catch (err) {
        console.error(err);
        alert("Có lỗi xảy ra khi thanh toán PayPal");
        paypalBtn.disabled = false;
        paypalBtn.innerText = "PayPal";
    }
});