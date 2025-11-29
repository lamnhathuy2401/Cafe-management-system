/*
Đề:
function calculatePrice(product) {

    let price = product.price;

    if (product.type === "electronics") {
        price = price - price * 0.1;
    } else if (product.type === "clothing") {
        price = price - price * 0.2;
    } else if (product.type === "food") {
        price = price - price * 0.05;
    }

    if (product.quantity > 10) {
        price = price - 5;
    }

    if (product.isMember === true) {
        price = price - 10;
    }

    return price; 
}

Yêu cầu:
1. Loại bỏ if...else lồng nhau
2. Tách logic giảm giá theo loại hàng ra hàm riêng
3. Sử dụng cấu trúc dữ liệu để thay magic numbers
4. Làm code dễ đọc & dễ mở rộng
*/


// Bảng cấu hình giảm giá theo loại sản phẩm
const sp = {
    electronics: 0.10,
    clothing: 0.20,
    food: 0.00
};

// Giảm giá thành viên cố định
const MEMBER_DISCOUNT = 10;

// Giảm giá số lượng lớn
const BULK_DISCOUNT = 5;

// Giảm giá VAT chung cho tất cả sản phẩm
const GENERAL_DISCOUNT = 0.05;


// Hàm tính giảm giá theo loại sản phẩm
function getCategoryDiscount(type) {
    return sp[type] ?? 0;
}


// Hàm tính giá cuối cùng của sản phẩm sau các loại giảm giá
function calculatePrice(product) {
    let price = product.price;

    // Giảm theo loại hàng
    const categoryRate = getCategoryDiscount(product.type);
    price -= price * categoryRate;

    // Giảm chung 5%
    price -= price * GENERAL_DISCOUNT;

    // Giảm khi mua số lượng nhiều
    if (product.quantity > 10) {
        price -= BULK_DISCOUNT;
    }

    // Giảm cho thành viên
    if (product.isMember === true) {
        price -= MEMBER_DISCOUNT;
    }

    return price;
}
