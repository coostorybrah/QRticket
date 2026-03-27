import { createOrder, addItems, getPaymentUrl } from "./api.js";

export function initCheckout(form, payBtn, getItems) {
    let isProcessing = false;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        if (!form.checkValidity()) {
            form.reportValidity(); // shows browser errors
            return;
        }

        if (isProcessing) return;
        isProcessing = true;

        const items = getItems();
        
        // DEBUGGING
        console.log("ITEMS SENT TO BACKEND:", items);

        if (items.length === 0) {
            alert("Vui lòng chọn ít nhất 1 vé");
            isProcessing = false;
            return;
        }

        payBtn.disabled = true;
        payBtn.innerText = "Đang xử lý...";

        try {
            const buyerName = document.getElementById("buyerName").value;
            const buyerEmail = document.getElementById("buyerEmail").value;
            const buyerPhone = document.getElementById("buyerPhone").value;

            const data = await createOrder({
                buyer_name: buyerName,
                buyer_email: buyerEmail,
                buyer_phone: buyerPhone
            });

            const orderId = data.order_id;

            await addItems(orderId, items);

            // Get VNPay URL
            const paymentData = await getPaymentUrl(orderId);
            if (!paymentData || !paymentData.payment_url) {
                throw new Error("Invalid payment URL");
            }
            
            // Redirect to VNPay
            window.location.href = paymentData.payment_url;

        } catch (err) {
            console.error(err);
            alert("Có lỗi xảy ra");
            isProcessing = false;
            payBtn.disabled = false;
            payBtn.innerText = "Thanh toán";
        }
    });
}