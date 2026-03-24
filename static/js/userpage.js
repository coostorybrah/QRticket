// CSRF
function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

// AVATAR
export function initAvatarUpload() {
    const avatarImg = document.getElementById("avatar");
    const fileInput = document.getElementById("avatarInput");

    if (!avatarImg || !fileInput) return;

    const wrapper = avatarImg.parentElement;
    let isUploading = false;

    // click avatar → open file picker
    wrapper.addEventListener("click", () => {
        if (!isUploading) fileInput.click();
    });

    // handle file selection
    fileInput.addEventListener("change", async () => {
        const file = fileInput.files[0];
        if (!file) return;

        if (!file.type.startsWith("image/")) {
            alert("Chỉ được chọn file ảnh");
            fileInput.value = "";
            return;
        }

        if (file.size > 2 * 1024 * 1024) {
            alert("Ảnh tối đa 2MB");
            fileInput.value = "";
            return;
        }

        if (isUploading) return;
        isUploading = true;

        const formData = new FormData();
        formData.append("avatar", file);

        wrapper.classList.add("uploading");

        try {
            const res = await fetch("/api/upload-avatar/", {
                method: "POST",
                body: formData,
                headers: { "X-CSRFToken": getCSRFToken() }
            });

            const data = await res.json();

            if (data.success) {
                location.reload();
            } else {
                alert(data.error);
            }

        } catch (err) {
            alert("Lỗi kết nối server");
        }

        wrapper.classList.remove("uploading");
        fileInput.value = "";
        isUploading = false;
    });
}

// USERNAME
export function initUsernameUpdate() {
    const form = document.getElementById("userInfoForm");
    if (!form) return;

    const btn = form.querySelector("button");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = form.username.value.trim();

        if (!username) {
            return alert("Username không được để trống");
        }

        btn.disabled = true;

        try {
            const res = await fetch("/api/update-username/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ username })
            });

            const data = await res.json();

            if (data.success) {
                alert("Cập nhật thành công");

            }
            else {
                alert(data.error);
            }

        }
        catch (err) {
            alert("Lỗi kết nối server");
        }

        btn.disabled = false;
    });
}

// PASSWORD
export function initPasswordChange() {
    const form = document.getElementById("passwordForm");
    if (!form) return;

    const btn = form.querySelector("button");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const current = form.current_password.value;
        const newPass = form.new_password.value;
        const confirm = form.confirm_password.value;

        if (newPass !== confirm) {
            return alert("Mật khẩu xác nhận không khớp");
        }

        if (newPass.length < 6) {
            return alert("Mật khẩu phải >= 6 ký tự");
        }

        btn.disabled = true;

        try {
            const res = await fetch("/api/change-password/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({
                    current_password: current,
                    new_password: newPass,
                    confirm_password: confirm
                })
            });

            const data = await res.json();

            if (data.success) {
                alert("Đổi mật khẩu thành công");
                form.reset();
            }
            else {
                alert(data.error);
            }

        }
        catch (err) {
            alert("Lỗi kết nối server");
        }

        btn.disabled = false;
    });
}