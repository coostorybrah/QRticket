import { formatPrice } from "../modules/formatPrice.js";

export function updateTotalUI(totalPriceEl, payBtn, total) {
    payBtn.disabled = total === 0;
    totalPriceEl.innerText = formatPrice(total);
}

export function renderEvent(event, nameEl, imgEl) {
    nameEl.innerText = event.ten;
    imgEl.src = event.anh;
}