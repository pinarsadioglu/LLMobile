document.addEventListener("click", function(event) {
    if (event.target && event.target.id === "deleteScan") {
        event.preventDefault();

        var apkId = event.target.getAttribute("data-apk-id");
        var row = $('#apk-' + apkId); // İlgili satır

        // AJAX isteği gönderme
        fetch(`/delete-scan/${apkId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Scan başarıyla silindi!") {
                // Başarılı ise satırı geçişli olarak sil
                row.fadeOut(1000, function() {
                    $(this).remove();
                });
                var toast = document.getElementById("toast");
                toast.classList.add("show");
                toast.style.display = "block";

                // 3 saniye sonra toast mesajını gizle
                setTimeout(function() {
                    toast.classList.remove("show");
                    toast.style.display = "none";
                }, 5000);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Hata:', error);
        });
    }
});

document.addEventListener("click", function(event) {
    if (event.target && event.target.id === "result") {
    event.preventDefault();  // Sayfa yenilenmesini engelle
    var apkId = event.target.getAttribute("data-apk-id");
    // Cookie ayarlama (örneğin, 1 gün sonra süresi dolacak bir cookie)
    var cookieName = "apk_id";
    var cookieValue = apkId;
    var expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + 7);  // 1 gün sonra süresi dolacak
    
    document.cookie = cookieName + "=" + cookieValue + "; expires=" + expirationDate.toUTCString() + "; path=/";
    window.location.href = "/manifest-analysis.html"

}});
