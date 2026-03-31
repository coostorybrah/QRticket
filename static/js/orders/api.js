import { apiFetch } from "../modules/generalApi.js";


// GET EVENT DATA
export function fetchEvent(eventId) {
    return apiFetch(`/api/events/${eventId}/`);
}


// CREATE ORDER
export function createOrder(data) {
    return apiFetch("/api/orders/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}


// ADD TICKETS TO ORDER
export function addItems(orderId, items) {
    return apiFetch(`/api/orders/${orderId}/items/`, {
        method: "POST",
        body: JSON.stringify({ items }),
    });
}


// PAYMENT URL
export function getPaymentUrl(orderId) {
    return apiFetch(`/api/orders/${orderId}/pay/`, {
        method: "GET",
    });
}