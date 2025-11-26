// static/js/cart_manager.js - Backend-ի կողմից կառավարվող զամբյուղի համար

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


// --- ԾԱՆՈՒՑՄԱՆ ՖՈՒՆԿՑԻԱ (ՊԱՐԶ ALERT) ---

/**
 * Ցուցադրում է պարզ ծանուցումը alert-ի միջոցով։
 */
function showOrderSuccessMessage(orderId, totalAmount) {
    const message = `
🎉 ՊԱՏՎԵՐԸ ՀԱՋՈՂՈՒԹՅԱՄԲ ԱՎԱՐՏՎԵՑ!

🔢 Պատվերի համար: #${orderId}
💰 Ընդհանուր գումար: ${totalAmount.toFixed(2)} ֏

Շնորհակալություն գնումների համար:
    `;

    // Օգտագործում ենք ստանդարտ alert(), որը կապահովի, որ հաղորդագրությունը երևա:
    alert(message.trim());
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

            // 1. ՑՈՒՑԱԴՐԵԼ ԾԱՆՈՒՑՈՒՄԸ (Կարգելափակի էջը մինչև OK սեղմելը)
            showOrderSuccessMessage(result.id, result.total_amount);

            // 2. ՎԵՐԱՀՂՈՒՄԸ ԿԱՏԱՐՎՈՒՄ Է alert-ը ՓԱԿԵԼՈՒՑ ՀԵՏՈ
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