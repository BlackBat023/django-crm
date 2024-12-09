let items = [];

function renderItems() {
    const container = document.getElementById('orderItems');
    container.innerHTML = '';
    let totalCost = 0;

    items.forEach((item, index) => {
        const itemDiv = document.createElement('div');
        itemDiv.innerHTML = `
            <select class="form-select" onchange="updateItem(${index}, 'item_name', this.value)">
                <option value="" selected>Select Product</option>
                ${['Rooikrans', 'Black Wattle', 'Bloekom', 'Myrtle', 'R65 RK', 'R30 RK', 'R45 BW', 'R45 BK', 'R45 K/D', 'R80 K/D', 'R45 Sekel', 'R80 Sekel', 'R45 SH', 'R80 SH', 'R80 MP', 'Blitz', 'R20 Starters'].map(option =>
                    `<option value="${option}" ${item.item_name === option ? 'selected' : ''}>${option}</option>`
                ).join('')}
            </select>
            <label for="quantity">Quantity</label>
            <input id="quantity" class="form-control" type="number" value="${item.quantity}" placeholder="Quantity" onchange="updateItem(${index}, 'quantity', this.value)"><br/>
            <label for="unit_price">Unit Price</label>
            <input id="unit_price" class="form-control" type="number" step="0.01" value="${item.unit_price}" placeholder="Unit Price" onchange="updateItem(${index}, 'unit_price', this.value)"><br/>
            <label for="delivery_price">Delivery Fee</label>
            <input id="delivery_price" class="form-control" type="number" step="0.01" value="${item.delivery_price}" placeholder="Delivery Price" onchange="updateItem(${index}, 'delivery_price', this.value)"><br/>
            <span>Total: R${item.total_price}</span><br/>
            <button class="btn btn-dark" onclick="removeItem(${index})">Remove</button>
        `;
        container.appendChild(itemDiv);
        totalCost += parseFloat(item.total_price);
    });

    const totalDiv = document.createElement('div');
    totalDiv.innerHTML = `<strong>Total Cost: R${totalCost.toFixed(2)}</strong>`;
    container.appendChild(totalDiv);
}

function addItem() {
    items.push({
        item_name: '',
        quantity: 0,
        unit_price: 0,
        delivery_price: 0,
        total_price: 0
    });
    renderItems();
}

function updateItem(index, field, value) {
    items[index][field] = value;
    if (field !== 'item_name') {
        calculateItemTotal(index);
    }
    renderItems();
}

function calculateItemTotal(index) {
    const item = items[index];
    item.total_price = (parseFloat(item.unit_price) * parseInt(item.quantity) + parseFloat(item.delivery_price)).toFixed(2);
}

function removeItem(index) {
    items.splice(index, 1);
    renderItems();
}

document.getElementById('addItem').addEventListener('click', addItem);

document.getElementById('orderForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    formData.append('items_data', JSON.stringify(items));

    fetch(this.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if(!response.ok) {
            return response.text().then(text => {
                throw new Error(`HTTP error! status: ${response.status}, message: ${text}`);
            });
        }
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
            return response.json();
        } else {
            throw new Error("Oops, we haven't received a JSON response");
        }
    })
    .then(data => {
        if (data.success) {
            window.location.href = `/orders/${data.order_id}/`;
        } else {
            console.error('Error: ', data.errors);
            alert('Error: ' + JSON.stringify(data.errors));
        }
    }).catch(error => {
        console.error('Error: ', error);
        alert('An error occorred: ' + error.message);
    });
});

renderItems();