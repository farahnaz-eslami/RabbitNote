var flag = 0
function coverit() {
    if (flag == 0) {
        document.getElementById("signup-form").style.width = "90%";
        function create_timeout() {
            document.getElementById("cover").style.display = "none";
        }
        document.getElementById("cover").style.opacity = "0";
        setTimeout(create_timeout, 1000);
        document.getElementById("change-btn").innerHTML = "از قبل حساب دارم";
        flag = 1
    }
    else {
        document.getElementById("signup-form").style.width = "10%";
        document.getElementById("cover").style.display = "block";
        document.getElementById("cover").style.opacity = "1";
        document.getElementById("change-btn").innerHTML = "ایجاد حساب جدید";
        flag = 0
    }  
}