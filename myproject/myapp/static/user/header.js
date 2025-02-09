document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");
    const overlay = document.querySelector(".overlay");

    // Toggle menu khi nhấn nút hamburger
    menuToggle.addEventListener("click", () => {
        navLinks.classList.toggle("active");
        overlay.classList.toggle("active");
    });

    // Ẩn menu khi nhấn overlay
    overlay.addEventListener("click", () => {
        navLinks.classList.remove("active");
        overlay.classList.remove("active");
    });
});

// document.addEventListener("DOMContentLoaded", function () {
//     const overlay = document.querySelector(".overlay");
//     const nav_links = document.querySelector(".nav-links");
//     const spinner = document.getElementById("loading-spinner");
//     const links = document.querySelectorAll("a"); // Lấy tất cả các liên kết

//     links.forEach(link => {
//         link.addEventListener("click", function (event) {
//             event.preventDefault(); // Ngăn chặn hành động mặc định (ngay lập tức chuyển trang)
//             const href = this.getAttribute("href"); // Lấy đường dẫn của liên kết
            
//             if (!overlay.classList.contains('active')) {
//                 overlay.classList.add("active");
//             }
//             if(nav_links.classList.contains("active")){
//                 nav_links.classList.remove("active")
//             }          
//             spinner.style.display = "block";

//             // Delay trước khi điều hướng
//             setTimeout(function () {
//                 window.location.href = href; // Điều hướng đến trang mới
//                 overlay.classList.remove("active");
//                 spinner.style.display = "none";
//             }, 3000); // 3000ms = 3 giây
//         });
//     });
// });

  