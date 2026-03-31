export function formatPrice(price){
    return price.toLocaleString("vi-VN") + "đ";
}

export function formatDate(dateStr) {
    if (!dateStr) return "";

    const date = new Date(dateStr);

    if (isNaN(date)) return "";

    return date.toLocaleDateString("vi-VN", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric"
    });
}

export function formatTime(timeStr) {
    if (!timeStr) return "";

    const date = new Date(`1970-01-01T${timeStr}`);

    if (isNaN(date)) return "";

    return date.toLocaleTimeString("vi-VN", {
        hour: "2-digit",
        minute: "2-digit"
    });
}