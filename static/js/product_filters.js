
// static/js/product_filters.js

// Օժանդակ ֆունկցիաներ
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function escapeHTML(str) {
    // Պաշտպանություն XSS-ից
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// Ֆունկցիա՝ կատեգորիաները բեռնելու և ցուցադրելու համար (ՉՓՈԽՎԱԾ)
async function loadCategories(initialCategoryId) {
    const categoryFiltersDiv = document.getElementById('category-filters');
    const categoriesLoadingMessage = document.getElementById('categories-loading-message');
    const errorMessage = document.getElementById('error-message');

    if (categoriesLoadingMessage) categoriesLoadingMessage.classList.remove('hidden');

    try {
        const response = await fetch('/category/');
        if (!response.ok) {
            throw new Error('Կատեգորիաները բեռնելիս սխալ: ' + response.status);
        }
        const categories = await response.json();

        if (categoriesLoadingMessage) categoriesLoadingMessage.classList.add('hidden');

        categories.forEach(category => {
            const button = document.createElement('button');
            const isActive = parseInt(category.id) === initialCategoryId;

            button.classList.add(
                'filter-btn', 'px-4', 'py-2', 'font-semibold', 'rounded-full', 'shadow-sm',
                'transition-all', 'text-sm'
            );

            if (isActive) {
                button.classList.add('bg-indigo-600', 'text-white', 'hover:bg-indigo-700');
            } else {
                button.classList.add('bg-gray-200', 'text-gray-700', 'hover:bg-indigo-100', 'hover:text-indigo-700');
            }

            button.textContent = escapeHTML(category.name);
            button.dataset.categoryId = category.id;

            if (categoryFiltersDiv) categoryFiltersDiv.appendChild(button);
        });

        addFilterButtonListeners();

    } catch (error) {
        console.error('Error loading categories:', error);
        if (categoriesLoadingMessage) {
            categoriesLoadingMessage.textContent = 'Կատեգորիաները բեռնել չհաջողվեց։';
            categoriesLoadingMessage.classList.remove('hidden');
        }
        if (errorMessage) errorMessage.textContent = 'Կատեգորիաների բեռնման խնդիր։';
        if (errorMessage) errorMessage.classList.remove('hidden');
    }
}


// Ֆունկցիա՝ ապրանքները բեռնելու և ցուցադրելու համար (ՓՈԽՎԱԾ՝ ՔԱՆԱԿՆԵՐԻ ՀԱՄԱՐ)
async function loadProducts(categoryId = 0) {
    const productsListDiv = document.getElementById('products-list');
    const loadingMessage = document.getElementById('loading-message');
    const errorMessage = document.getElementById('error-message');

    if (!productsListDiv || !loadingMessage) return;

    loadingMessage.classList.remove('hidden');
    errorMessage.classList.add('hidden');
    productsListDiv.innerHTML = '';

    let url = '/products/AllProducts';
    if (categoryId !== 0) {
        url += `?category_id=${categoryId}`;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Ապրանքները բեռնելիս սխալ: ' + response.status);
        }
        const products = await response.json();

        loadingMessage.classList.add('hidden');

        if (products.length === 0) {
            productsListDiv.innerHTML = '<p class="col-span-full text-center text-gray-500 mt-10 text-xl">Այս կատեգորիայում ապրանքներ չկան։</p>';
            return;
        }

        products.forEach(product => {
            const productCard = document.createElement('div');
            productCard.classList.add(
                'bg-white', 'rounded-xl', 'shadow-lg', 'overflow-hidden',
                'transform', 'hover:scale-[1.02]', 'transition-transform', 'duration-300',
                'border', 'border-gray-100', 'flex', 'flex-col'
            );

            // Ստուգում ենք պահեստային քանակը
            const isInStock = (product.stock_quantity || 0) > 0;
            const stockMessageClass = isInStock ? 'text-green-600' : 'text-red-600';
            const stockQuantity = product.stock_quantity || 0;

            productCard.innerHTML = `
                <img src="${escapeHTML(product.img_url || '/images/default_product.png')}" alt="${escapeHTML(product.name)}" class="w-full h-48 object-cover">

                <div class="p-5 flex-grow">
                    <h3 class="text-xl font-bold text-gray-800 mb-2">${escapeHTML(product.name)}</h3>
                    <p class="text-gray-500 text-sm mb-3">${escapeHTML(product.description || 'Նկարագրություն բացակայում է։')}</p>

                    <div class="flex items-center justify-between mb-2">
                        <span class="text-2xl font-bold text-indigo-700">${product.price} ֏</span>
                        <span class="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">${escapeHTML(product.category.name)}</span>
                    </div>

                    <div class="mb-4">
                        <p class="text-sm font-semibold ${stockMessageClass}">
                            Պահեստում: ${isInStock ? stockQuantity + ' հատ' : 'Սպառված է 🚫'}
                        </p>
                    </div>
                </div>

                <div class="p-5 pt-0 border-t border-gray-100">
                    ${isInStock
                        ? `
                        <div class="flex items-center justify-between gap-3">

                            <input type="number"
                                   value="1"
                                   min="1"
                                   max="${stockQuantity}"
                                   id="quantity-input-${product.id}" // 👈 ԿԱՐԵՎՈՐ ՓՈՓՈԽՈՒԹՅՈՒՆ
                                   data-product-id="${product.id}"
                                   class="quantity-input w-20 px-3 py-2 border border-gray-300 rounded-lg text-center text-gray-700 focus:ring-indigo-500 focus:border-indigo-500"
                                   aria-label="Նշել գնվող քանակը">

                            <button data-product-id="${product.id}"
                                    data-product-name="${escapeHTML(product.name)}"
                                    data-product-price="${product.price}"
                                    class="add-to-cart-btn flex-grow px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-colors">
                                Ավելացնել զամբյուղ 🛒
                            </button>
                        </div>
                        `
                        : `
                        <button disabled
                                class="w-full px-4 py-2 bg-gray-400 text-white font-semibold rounded-lg cursor-not-allowed">
                            Սպասում ենք համալրման
                        </button>
                        `
                    }
                </div>
            `;
            productsListDiv.appendChild(productCard);
        });

        // ԿԱՐԵՎՈՐ ԼՈՒԾՈՒՄ: Կցել listener-ները ԱՊՐԱՆՔՆԵՐԸ ԲԵՌՆԵԼՈՒՑ ՀԵՏՈ
        if (typeof setupAddToCartListeners === 'function') {
            setupAddToCartListeners();
        }


    } catch (error) {
        console.error('Error loading products:', error);
        if (loadingMessage) loadingMessage.classList.add('hidden');
        if (errorMessage) {
            errorMessage.textContent = 'Ապրանքները բեռնել չհաջողվեց։ Խնդրում ենք կրկին փորձել։';
            errorMessage.remove('hidden');
        }
        if (productsListDiv) productsListDiv.innerHTML = '';
    }
}


// Ֆունկցիա՝ ֆիլտրի կոճակներին listener-ներ ավելացնելու համար (ՉՓՈԽՎԱԾ)
function addFilterButtonListeners() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const categoryId = parseInt(button.dataset.categoryId);

            loadProducts(categoryId);

            filterButtons.forEach(btn => {
                btn.classList.remove('bg-indigo-600', 'text-white', 'hover:bg-indigo-700');
                btn.classList.add('bg-gray-200', 'text-gray-700', 'hover:bg-indigo-100', 'hover:text-indigo-700');
            });
            button.classList.remove('bg-gray-200', 'text-gray-700', 'hover:bg-indigo-100', 'hover:text-indigo-700');
            button.classList.add('bg-indigo-600', 'text-white', 'hover:bg-indigo-700');
        });
    });
}


// Էջի Սկզբնական Գործարկումը (ՉՓՈԽՎԱԾ)
const initialCategoryId = parseInt(getQueryParam('category_id') || '0');

loadCategories(initialCategoryId).then(() => {
    loadProducts(initialCategoryId);

    if (initialCategoryId === 0) {
        const allButton = document.getElementById('filter-all');
        if (allButton) {
            allButton.classList.remove('bg-gray-200', 'text-gray-700', 'hover:bg-indigo-100', 'hover:text-indigo-700');
            allButton.classList.add('bg-indigo-600', 'text-white', 'hover:bg-indigo-700');
        }
    }
});