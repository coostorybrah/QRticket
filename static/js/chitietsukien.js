import { formatPrice } from "./modules/format.js";
import { publicFetch } from "./modules/generalApi.js";

const id = event_id;

try {
    const event = await publicFetch(`/api/events/${id}/`);

    if (!event || event.error) {
        throw new Error("Event not found");
    }

    document.getElementById("tenSuKien").innerText = event.ten;
    document.getElementById("anhBanner").src = event.anh;
    document.getElementById("displayDate").innerText = event.displayDate + ": ";
    document.getElementById("startTime").innerText = event.startTime + " - ";
    document.getElementById("endTime").innerText = event.endTime;
    document.getElementById("diaChiTen").innerText = event.dcTen;
    document.getElementById("diaChiCuThe").innerText = event.dcCuThe;
    document.getElementById("giaVe").innerText = formatPrice(event.giaMin);
    document.getElementById("moTa").innerHTML = event.moTa;

    let ticketsHTML = `
        <tr>
            <th align='left'>Loại vé</th>
            <th align='right'>Giá vé</th>
        </tr>`;

    event.tickets.forEach(ticket => {
        ticketsHTML += `
        <tr>
            <td>${ticket.loai}</td>
            <td align="right">${formatPrice(ticket.gia)}</td>
        </tr>`;
    });

    document.getElementById("bangGiaVe").innerHTML = ticketsHTML;
    document.title = "QRticket | " + event.ten;

} catch (err) {
    console.error(err);
    document.body.innerHTML = "<div align='center'>Sự kiện không tồn tại.</div>";
}