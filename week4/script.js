// checkbox 沒勾就不可以送
document.getElementById("login-form").addEventListener("submit", function(event) {
    var checkbox = document.getElementById("agree");
    if (!checkbox.checked) {
        event.preventDefault();
        alert("請勾選同意條款");
    }
});

// 旅館查詢，要是正整數才能過
document.getElementById("hotel-btn").addEventListener("click", function() {
    var idValue = document.getElementById("hotel-id").value;
    var num = Number(idValue);
    if (!idValue || !Number.isInteger(num) || num <= 0) {
        alert("請輸入正整數");
    } else {
        window.location.href = "/hotel/" + num;
    }
});