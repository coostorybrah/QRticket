import { formatPrice } from "./modules/format.js";
import { publicFetch } from "./modules/generalApi.js";

async function loadEvents() {
    // TRÍCH DỮ LIỆU TỪ CSDL (.json)
    const db = await publicFetch("/api/events/", {method: "GET"});

    // TRẢ CARD THEO THỂ LOẠI
    Object.entries(db).forEach(([id, item]) => {
        item.categories.forEach( category => {
            const container = document.getElementById(category);
            if (!container) {
            return; 
            } 

            const card = `
            <div class="card">
                <div class="card__image">
                    <a href="/chitietsukien/${id}">
                        <img src="${item.anh}">
                    </a>
                </div>

                <div class="card__description">
                    <a href="/chitietsukien/${id}" class="card__description__name">${item.ten}</a>
                    <span class="card__description__price">Từ ${formatPrice(item.giaMin)}</span>
                    <span class="card__description__date">Ngày ${item.displayDate} |
                        <span class="card__description__time"> ${item.startTime} - ${item.endTime}</span>
                    </span>
                </div>
            </div>
            `;
            container.insertAdjacentHTML("beforeend", card);
        });
    });
}

loadEvents();