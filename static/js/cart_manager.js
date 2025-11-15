// static/js/cart_manager.js - Ամբողջությամբ փոփոխված Backend-ի կողմից կառավարվող զամբյուղի համար

/**
 * Որոշում է օգտատիրոջ ինդենտիֆիկատորը (Session ID), որը կուղարկվի Header-ով։
 */
function getUserIdentifier() {
    let userId = localStorage.getItem('user_session_id');
    if (!userId) {
        // Գեներացնում ենք պարզ UUID.
        userId = 'user-' + Math.random().toString(36).substring(2, 11);
        localStorage.setItem('user_session_id', userId);
    }
    return userId;
}

const USER_ID = getUserIdentifier();


// --- ԶԱՄԲՅՈՒՂԻ CORE ՖՈՒՆԿՑԻԱՆԵՐ (API-ի վրա հիմնված) ---

/**
 * Բերում է զամբյուղի ընթացիկ տվյալները Backend-ից։
 */
async function fetchCart() {
    try {
        const response = await fetch('/cart/', {
            method: 'GET',
            headers: {
                'X-User-Identifier': USER_ID, // Ուղարկում ենք Header-ը
            }
        });
        if (!response.ok) throw new Error('Failed to fetch cart data.');
        const cartData = await response.json();
        return cartData;
    } catch (error) {
        console.error('Error fetching cart:', error);
        return { items: [], total_amount: 0.0 };
    }
}

/**
 * Թարմացնում է զամբյուղի քանակը վերնագրում։
 */
async function updateCartCount() {
    const cart = await fetchCart();
    const totalItems = cart.items.reduce((total, item) => total + item.quantity, 0);

    const cartCountElement = document.getElementById('cart-item-count');

    if (cartCountElement) {
        cartCountElement.textContent = totalItems;
        if (totalItems > 0) {
            cartCountElement.classList.remove('hidden');
        } else {
            cartCountElement.classList.add('hidden');
        }
    }
    return cart;
}


/**
 * Ավելացնում/Փոխում է ապրանքի քանակը զամբյուղում (Backend API)։
 */
async function addToCart(productId, name, price, quantity = 1) {
    try {
        const response = await fetch('/cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-User-Identifier': USER_ID,
            },
            body: JSON.stringify({ product_id: productId, quantity: quantity })
        });

        const result = await response.json();

        if (response.ok) {
            updateCartCount();
            // 🚫 ՀԱՋՈՂՈՒԹՅԱՆ ԾԱՆՈՒՑՈՒՄԸ ՀԵՌԱՑՎԱԾ Է
        } else {
            // Ցույց տալ backend-ի կողմից ուղարկված սխալը (օրինակ՝ պահեստի պակաս)
            alert(`⚠️ Զամբյուղում ավելացնելիս սխալ: ${result.detail || 'Խնդրում ենք փորձել նորից։'}`);
            console.error('Add to cart failed:', result);
        }

    } catch (error) {
        console.error('Network or server error:', error);
        alert("🛑 Ցանցային սխալ։");
    }
}

/**
 * Կցում է Listener-ները բոլոր Add-to-Cart կոճակներին։
 */
function setupAddToCartListeners() {
    const buttons = document.querySelectorAll('.add-to-cart-btn');

    buttons.forEach(button => {
        if (!button.hasAttribute('data-listener-added')) {
            button.addEventListener('click', (event) => {
                const productId = parseInt(button.dataset.productId);
                const name = button.dataset.productName;
                const price = parseFloat(button.dataset.productPrice);

                const quantityInput = document.getElementById(`quantity-input-${productId}`);
                let quantity = 1;
                if (quantityInput) {
                    quantity = parseInt(quantityInput.value) || 1;
                    const maxQuantity = parseInt(quantityInput.max);
                    if (quantity < 1) quantity = 1;
                    if (quantity > maxQuantity) quantity = maxQuantity;
                }

                if (productId && name && price) {
                    addToCart(productId, name, price, quantity);
                } else {
                    console.error("Missing product data for add to cart button.");
                }
            });
            button.setAttribute('data-listener-added', 'true');
        }
    });
}


// --- CHECKOUT (ՊԱՏՎԻՐԵԼ) ---
async function submitOrder() {
    const USER_ID = getUserIdentifier();

    const cart = await fetchCart();
    if (cart.items.length === 0) {
        alert("Զամբյուղը դատարկ է։ Խնդրում ենք ավելացնել ապրանքներ։");
        return;
    }

    try {
        const response = await fetch('/orders/', {
            method: 'POST',
            headers: {
                'X-User-Identifier': USER_ID,
            }
        });

        const result = await response.json();

        if (response.ok) {
            updateCartCount();
            // 🚫 ՊԱՏՎԵՐԻ ՀԱՋՈՂՈՒԹՅԱՆ ԾԱՆՈՒՑՈՒՄԸ ՀԵՌԱՑՎԱԾ Է
            window.location.href = '/';
        } else {
            alert(`🛑 Պատվերի սխալ: ${result.detail || 'Խնդրում ենք փորձել նորից։'}`);
            console.error('Order creation failed:', result);
        }

    } catch (error) {
        console.error('Network or server error during checkout:', error);
        alert("🛑 Ցանցային սխալ։");
    }
}

// Էջի բեռնումից հետո աշխատում է միայն զամբյուղի հաշվիչը
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    setupAddToCartListeners();
});


//
//// static/js/cart_manager.js - Ամբողջությամբ փոփոխված Backend-ի կողմից կառավարվող զամբյուղի համար
//
///**
// * Որոշում է օգտատիրոջ ինդենտիֆիկատորը (Session ID), որը կուղարկվի Header-ով։
// */
//function getUserIdentifier() {
//    let userId = localStorage.getItem('user_session_id');
//    if (!userId) {
//        // Գեներացնում ենք պարզ UUID.
//        userId = 'user-' + Math.random().toString(36).substring(2, 11);
//        localStorage.setItem('user_session_id', userId);
//    }
//    return userId;
//}
//
//const USER_ID = getUserIdentifier();
//
//
//// --- ԶԱՄԲՅՈՒՂԻ CORE ՖՈՒՆԿՑԻԱՆԵՐ (API-ի վրա հիմնված) ---
//
///**
// * Բերում է զամբյուղի ընթացիկ տվյալները Backend-ից։
// */
//async function fetchCart() {
//    try {
//        const response = await fetch('/cart/', {
//            method: 'GET',
//            headers: {
//                'X-User-Identifier': USER_ID, // Ուղարկում ենք Header-ը
//            }
//        });
//        if (!response.ok) throw new Error('Failed to fetch cart data.');
//        const cartData = await response.json();
//        return cartData;
//    } catch (error) {
//        console.error('Error fetching cart:', error);
//        return { items: [], total_amount: 0.0 };
//    }
//}
//
///**
// * Թարմացնում է զամբյուղի քանակը վերնագրում։
// */
//async function updateCartCount() {
//    const cart = await fetchCart();
//    const totalItems = cart.items.reduce((total, item) => total + item.quantity, 0);
//
//    const cartCountElement = document.getElementById('cart-item-count');
//
//    if (cartCountElement) {
//        cartCountElement.textContent = totalItems;
//        if (totalItems > 0) {
//            cartCountElement.classList.remove('hidden');
//        } else {
//            cartCountElement.classList.add('hidden');
//        }
//    }
//    return cart;
//}
//
//
///**
// * Ավելացնում/Փոխում է ապրանքի քանակը զամբյուղում (Backend API)։
// */
//async function addToCart(productId, name, price, quantity = 1) {
//    try {
//        const response = await fetch('/cart/', {
//            method: 'POST',
//            headers: {
//                'Content-Type': 'application/json',
//                'X-User-Identifier': USER_ID,
//            },
//            body: JSON.stringify({ product_id: productId, quantity: quantity })
//        });
//
//        const result = await response.json();
//
//        if (response.ok) {
//            updateCartCount();
//            // Օգտագործել custom alert կամ UI փոփոխություն
//            alert(`🛒 ${name} ավելացվեց զամբյուղին: Քանակը՝ ${quantity}`);
//        } else {
//            // Ցույց տալ backend-ի կողմից ուղարկված սխալը (օրինակ՝ պահեստի պակաս)
//            alert(`⚠️ Զամբյուղում ավելացնելիս սխալ: ${result.detail || 'Խնդրում ենք փորձել նորից։'}`);
//            console.error('Add to cart failed:', result);
//        }
//
//    } catch (error) {
//        console.error('Network or server error:', error);
//        alert("🛑 Ցանցային սխալ։");
//    }
//}
//
///**
// * Կցում է Listener-ները բոլոր Add-to-Cart կոճակներին։
// */
//function setupAddToCartListeners() {
//    const buttons = document.querySelectorAll('.add-to-cart-btn');
//
//    buttons.forEach(button => {
//        if (!button.hasAttribute('data-listener-added')) {
//            button.addEventListener('click', (event) => {
//                const productId = parseInt(button.dataset.productId);
//                const name = button.dataset.productName;
//                const price = parseFloat(button.dataset.productPrice);
//
//                const quantityInput = document.getElementById(`quantity-input-${productId}`);
//                let quantity = 1;
//                if (quantityInput) {
//                    quantity = parseInt(quantityInput.value) || 1;
//                    const maxQuantity = parseInt(quantityInput.max);
//                    if (quantity < 1) quantity = 1;
//                    if (quantity > maxQuantity) quantity = maxQuantity;
//                }
//
//                if (productId && name && price) {
//                    addToCart(productId, name, price, quantity);
//                } else {
//                    console.error("Missing product data for add to cart button.");
//                }
//            });
//            button.setAttribute('data-listener-added', 'true');
//        }
//    });
//}
//
//
//// --- CHECKOUT (ՊԱՏՎԻՐԵԼ) ---
//async function submitOrder() {
//    const USER_ID = getUserIdentifier();
//
//    const cart = await fetchCart();
//    if (cart.items.length === 0) {
//        alert("Զամբյուղը դատարկ է։ Խնդրում ենք ավելացնել ապրանքներ։");
//        return;
//    }
//
//    try {
//        const response = await fetch('/orders/', {
//            method: 'POST',
//            headers: {
//                'X-User-Identifier': USER_ID,
//            }
//        });
//
//        const result = await response.json();
//
//        if (response.ok) {
//            updateCartCount();
//            alert(`✅ Պատվերը #${result.id} հաջողությամբ տեղադրվեց! Ընդհանուր գումարը՝ ${result.total_amount.toFixed(2)} ֏`);
//
//            // Թարմացնել էջը
//            window.location.href = '/';
//        } else {
//            alert(`🛑 Պատվերի սխալ: ${result.detail || 'Խնդրում ենք փորձել նորից։'}`);
//            console.error('Order creation failed:', result);
//        }
//
//    } catch (error) {
//        console.error('Network or server error during checkout:', error);
//        alert("🛑 Ցանցային սխալ։");
//    }
//}
//
//// Էջի բեռնումից հետո աշխատում է միայն զամբյուղի հաշվիչը
//document.addEventListener('DOMContentLoaded', () => {
//    updateCartCount();
//    setupAddToCartListeners();
//});
//
//////async function submitOrder() {
//////    const orderData = prepareOrderData();
//////
//////    if (orderData.items.length === 0) {
//////        alert("Զամբյուղը դատարկ է։ Խնդրում ենք ավելացնել ապրանքներ։");
//////        return;
//////    }
//////
//////    try {
//////        const response = await fetch('/orders/', {
//////            method: 'POST',
//////            headers: {
//////                'Content-Type': 'application/json',
//////            },
//////            body: JSON.stringify(orderData)
//////        });
//////
//////        const result = await response.json();
//////
//////        if (response.ok) {
//////            localStorage.removeItem(CART_STORAGE_KEY);
//////            updateCartCount();
//////
//////            alert(`✅ Պատվերը #${result.id} հաջողությամբ տեղադրվեց! Ընդհանուր գումարը՝ ${result.total_amount.toFixed(2)} ֏`);
//////
//////            window.location.href = '/';
//////        } else {
//////            alert(`⚠️ Պատվեր տեղադրելիս սխալ տեղի ունեցավ։ ${result.detail || 'Խնդրում ենք փորձել նորից։'}`);
//////            console.error('Order submission failed:', result);
//////        }
//////    } catch (error) {
//////        console.error('Network or server error:', error);
//////        alert("🛑 Ցանցային սխալ։ Խնդրում ենք ստուգել ինտերնետ կապը։");
//////    }
//////}
//////
//////// Էջի բեռնումից հետո աշխատում է միայն զամբյուղի հաշվիչը (UI թարմացումը)
//////document.addEventListener('DOMContentLoaded', () => {
//////    updateCartCount();
//////});
////
////// static/js/cart_manager.js
////
////// Զամբյուղի տվյալների պահպանման և կառավարման տրամաբանությունը
////
////const CART_STORAGE_KEY = 'freshmarket_cart';
////
////// --- ԶԱՄԲՅՈՒՂԻ CORE ՖՈՒՆԿՑԻԱՆԵՐ ---
////
////function getCart() {
////    const cartJson = localStorage.getItem(CART_STORAGE_KEY);
////    try {
////        return cartJson ? JSON.parse(cartJson) : [];
////    } catch (e) {
////        console.error("Error parsing cart data from localStorage:", e);
////        return [];
////    }
////}
////
////function saveCart(cart) {
////    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
////    updateCartCount();
////}
////
////// --- ԿԱՐԵՎՈՐ ԶԱՄԲՅՈՒՂԻ ԳՈՐԾՈՂՈՒԹՅՈՒՆՆԵՐ ---
////
////function updateCartCount() {
////    const cart = getCart();
////    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
////
////    const cartCountElement = document.getElementById('cart-item-count');
////
////    if (cartCountElement) {
////        cartCountElement.textContent = totalItems;
////        if (totalItems > 0) {
////            cartCountElement.classList.remove('hidden');
////        } else {
////            cartCountElement.classList.add('hidden');
////        }
////    }
////}
////
////
/////**
//// * Ապրանքը զամբյուղին ավելացնելու կամ դրա քանակը մեծացնելու ֆունկցիա:
//// * @param {number} productId
//// * @param {string} name
//// * @param {number} price
//// * @param {number} quantity - Ընտրված քանակը (ՆՈՐ)
//// */
////function addToCart(productId, name, price, quantity = 1) { // 👈 ՖՈՒՆԿՑԻԱՆ ԸՆԴՈՒՆՈՒՄ Է ՔԱՆԱԿԸ
////    const cart = getCart();
////    const existingItem = cart.find(item => item.id === productId);
////
////    if (existingItem) {
////        // Եթե ապրանքն արդեն կա, ավելացնում ենք ընտրված քանակը
////        existingItem.quantity += quantity;
////        alert(`🛒 ${name}-ի քանակն ավելացվեց զամբյուղում: Ընդհանուր քանակը՝ ${existingItem.quantity}`);
////    } else {
////        // Եթե նոր է, ավելացնում ենք ընտրված քանակով
////        cart.push({
////            id: productId,
////            name: name,
////            price: price,
////            quantity: quantity // 👈 ՕԳՏԱԳՈՐԾՈՒՄ ԵՆՔ ՓՈԽԱՆՑՎԱԾ ՔԱՆԱԿԸ
////        });
////        alert(`🛒 ${name} ավելացվեց զամբյուղին: Քանակը՝ ${quantity}`);
////    }
////
////    saveCart(cart);
////}
////
/////**
//// * Event Listener-ը «Ավելացնել զամբյուղ» կոճակներին կցելու ֆունկցիա
//// */
////function setupAddToCartListeners() {
////    // Գտնում ենք բոլոր կոճակները, որոնք ունեն 'add-to-cart-btn' դասը
////    const buttons = document.querySelectorAll('.add-to-cart-btn');
////
////    buttons.forEach(button => {
////        // Միայն մեկ անգամ ենք ավելացնում listener-ը
////        if (!button.hasAttribute('data-listener-added')) {
////            button.addEventListener('click', (event) => {
////                const productId = parseInt(button.dataset.productId);
////                const name = button.dataset.productName;
////                const price = parseFloat(button.dataset.productPrice);
////
////                // 1. Գտնում ենք հարակից քանակի դաշտը ունիկալ ID-ի միջոցով
////                const quantityInput = document.getElementById(`quantity-input-${productId}`);
////
////                // 2. Վերցնում ենք արժեքը և վավերացնում
////                let quantity = 1;
////                if (quantityInput) {
////                    quantity = parseInt(quantityInput.value) || 1;
////
////                    // Պարզ վավերացում
////                    const maxQuantity = parseInt(quantityInput.max);
////                    if (quantity < 1) quantity = 1;
////                    if (quantity > maxQuantity) quantity = maxQuantity;
////                }
////
////                if (productId && name && price) {
////                    // 3. Կանչում ենք addToCart-ը՝ ՔԱՆԱԿՈՎ
////                    addToCart(productId, name, price, quantity);
////                } else {
////                    console.error("Missing product data for add to cart button.");
////                }
////            });
////            button.setAttribute('data-listener-added', 'true');
////        }
////    });
////}
////
////// --- CHECKOUT ԵՎ BACKEND ՀԱՂՈՐԴԱԿՑՈՒՄ (ՉՓՈԽՎԱԾ) ---
////
////function prepareOrderData() {
////    const cart = getCart();
////
////    const items = cart.map(item => ({
////        id: item.id,
////        quantity: item.quantity
////    }));
////
////    const orderData = {
////        items: items
////    };
////
////    return orderData;
////}
////
////async function submitOrder() {
////    const orderData = prepareOrderData();
////
////    if (orderData.items.length === 0) {
////        alert("Զամբյուղը դատարկ է։ Խնդրում ենք ավելացնել ապրանքներ։");
////        return;
////    }
////
////    try {
////        const response = await fetch('/orders/', {
////            method: 'POST',
////            headers: {
////                'Content-Type': 'application/json',
////            },
////            body: JSON.stringify(orderData)
////        });
////
////        const result = await response.json();
////
////        if (response.ok) {
////            localStorage.removeItem(CART_STORAGE_KEY);
////            updateCartCount();
////
////            alert(`✅ Պատվերը #${result.id} հաջողությամբ տեղադրվեց! Ընդհանուր գումարը՝ ${result.total_amount.toFixed(2)} ֏`);
////
////            window.location.href = '/';
////        } else {
////            alert(`⚠️ Պատվեր տեղադրելիս սխալ տեղի ունեցավ։ ${result.detail || 'Խնդրում ենք փորձել նորից։'}`);
////            console.error('Order submission failed:', result);
////        }
////    } catch (error) {
////        console.error('Network or server error:', error);
////        alert("🛑 Ցանցային սխալ։ Խնդրում ենք ստուգել ինտերնետ կապը։");
////    }
////}
////
////// Էջի բեռնումից հետո աշխատում է միայն զամբյուղի հաշվիչը
////document.addEventListener('DOMContentLoaded', () => {
////    updateCartCount();
////});