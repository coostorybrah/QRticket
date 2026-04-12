import { protectedFetch } from "../modules/generalApi.js";


// GET EVENT DATA
export function fetchEvent(eventId) {
    return protectedFetch(`/api/events/${eventId}/`);
}


// CREATE ORDER
export function createOrder(data) {
    return protectedFetch("/api/orders/", {
        method: "POST",
        body: JSON.stringify(data),
    });
}


// ADD TICKETS TO ORDER
export function addItems(orderId, items) {
    return protectedFetch(`/api/orders/${orderId}/items/`, {
        method: "POST",
        body: JSON.stringify({ items }),
    });
}


// PAYMENT URL
export function getPaymentUrl(orderId) {
    return protectedFetch(`/api/orders/${orderId}/pay/`, {
        method: "GET",
    });
}