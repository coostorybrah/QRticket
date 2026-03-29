import { apiFetch } from "./modules/generalApi.js";
import { requireAuth } from "./modules/authGuard.js";

let scanning = true; // 🔒 global lock

document.addEventListener("DOMContentLoaded", async () => {
    const allowed = await requireAuth();
    if (!allowed) return;

    const user = JSON.parse(localStorage.getItem("user"));

    // Allow only organizers
    if (!user?.is_organizer) {
        window.location.href = "/";
        return;
    }

    startScanner();
});


function startScanner() {
    const resultEl = document.getElementById("result");

    const scanner = new Html5Qrcode("video");

    scanner.start(
        { facingMode: "environment" },
        {
            fps: 10,
            qrbox: 250
        },
        async (decodedText) => {
            if (!scanning) return; // 🚫 prevent spam scans

            scanning = false; // 🔒 lock

            const ticketId = decodedText.split(":")[1];

            if (!ticketId) {
                resultEl.innerText = "QR không hợp lệ";
                return resetScanner(resultEl);
            }

            try {
                const data = await apiFetch("/api/orders/check-in/", {
                    method: "POST",
                    body: JSON.stringify({ ticket_id: ticketId })
                });

                if (data.status === "success") {
                    resultEl.innerText = "✅ Vé hợp lệ";
                } else if (data.error) {
                    resultEl.innerText = data.error;
                } else {
                    resultEl.innerText = "❌ Vé không hợp lệ";
                }

            } catch (err) {
                console.error(err);
                resultEl.innerText = "❌ Lỗi kiểm tra vé";
            }

            // ⏳ delay before next scan
            setTimeout(() => {
                resetScanner(resultEl);
            }, 2500);
        },
        (errorMessage) => {
            // ignore scan errors
        }
    );
}

function resetScanner(resultEl) {
    resultEl.innerText = "";
    scanning = true; // 🔓 unlock
}