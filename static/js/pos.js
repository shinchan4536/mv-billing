let cart = [];

function adjustQuickQty(amount) {
    let qtyInput = document.getElementById('search-qty');
    let currentVal = parseInt(qtyInput.value) || 1;
    if (currentVal + amount > 0) qtyInput.value = currentVal + amount;
}

function addSearchedItem() {
    let searchBox = document.getElementById('search-input');
    let qtyInput = document.getElementById('search-qty');
    let typedName = searchBox.value;
    let qty = parseInt(qtyInput.value) || 1;

    // INVENTORY is loaded from the HTML file!
    let product = INVENTORY.find(p => p.name === typedName);

    if (!product) return alert("Product not found! Select from the dropdown.");

    let existingItem = cart.find(item => item.id === product.id);
    if (existingItem) existingItem.qty += qty; 
    else cart.push({ id: product.id, name: product.name, price: product.price, qty: qty }); 

    searchBox.value = '';
    qtyInput.value = 1;
    searchBox.focus(); 
    updateCartUI();
}

function changeQty(id, amount) {
    let itemIndex = cart.findIndex(item => item.id === id);
    if (itemIndex !== -1) {
        cart[itemIndex].qty += amount;
        if (cart[itemIndex].qty <= 0) cart.splice(itemIndex, 1); 
        updateCartUI();
    }
}

function updateCartUI() {
    let cartBody = document.getElementById('cart-body');
    cartBody.innerHTML = ''; 
    cart.forEach(item => {
        let rowTotal = item.price * item.qty;
        cartBody.innerHTML += `
            <tr>
                <td><strong>${item.name}</strong><br><small class="text-muted">₹${item.price} each</small></td>
                <td class="text-center">
                    <button class="btn btn-sm btn-outline-danger px-2 py-0" onclick="changeQty(${item.id}, -1)">-</button>
                    <span class="mx-2 fw-bold">${item.qty}</span>
                    <button class="btn btn-sm btn-outline-success px-2 py-0" onclick="changeQty(${item.id}, 1)">+</button>
                </td>
                <td class="text-end text-dark fw-bold">₹${rowTotal.toFixed(2)}</td>
            </tr>
        `;
    });
    calculateMath();
}

function calculateMath() {
    let subTotal = 0;
    let totalTax = 0;

    cart.forEach(item => {
        let itemTotal = item.price * item.quantity;
        subTotal += itemTotal;
        if (item.gst) {
            let basePrice = itemTotal / (1 + (item.gst / 100));
            totalTax += (itemTotal - basePrice);
        }
    });

    let discount = parseFloat(document.getElementById('discount-input').value) || 0;
    let grandTotal = subTotal - discount;
    if (grandTotal < 0) grandTotal = 0;

    document.getElementById('sub-total').innerText = subTotal.toFixed(2);
    document.getElementById('grand-total').innerText = grandTotal.toFixed(2);
    
    let taxElement = document.getElementById('tax-total');
    if (taxElement) {
        taxElement.innerText = totalTax.toFixed(2);
    }
}

function processCheckout() {
    if (cart.length === 0) return alert("The cart is empty!");
    
    let cPhone = document.getElementById('cust-phone').value.trim();
    let cName = document.getElementById('cust-name').value.trim();
    let discount = parseFloat(document.getElementById('discount-input').value) || 0;

    if (cPhone === "" || cName === "") return alert("Please enter Customer Details!");

    // CHECKOUT_URL and REDIRECT_URL are loaded from the HTML file!
    fetch(CHECKOUT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            'cart': cart, 
            'discount': discount,
            'customer_phone': cPhone,
            'customer_name': cName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) alert("Checkout Failed: " + data.error);
        else {
            alert("Bill Saved Successfully!");
            // Teleport to the specific shop's receipt!
            window.location.href = `${REDIRECT_URL}${data.invoice_id}/`; 
        }
    });
}

