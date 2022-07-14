const table = document.getElementById("table-content");
const error_message = document.getElementById("error_message");
const error_alert = document.getElementById("error_alert")
const connected = document.getElementById("connected")

function clearRows() {
    table.innerHTML = "";
}

function appendRow(currency, method, treshold) {
    const row = document.createElement("tr")
    row.innerHTML = (`
    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900" >
        ${currency}
    </td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
        ${method}
    </td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
        ${treshold}
    </td>
        
    `);

    table.append(row);
}

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const loginButton = document.getElementById("login");



function init_table()
{
    axios.get(`http://127.0.0.1:8000/alert?mail=${emailInput.value}&password=${passwordInput.value}`).then((response) => {
        console.log(response.data);
        table.innerHTML = "";
        response.data.forEach((element) => {
            appendRow(element.currency, element.method, element.price);
        })

    }).catch((error) => {
        console.log(error);
    })
}

loginButton.onclick = () => {
    error_message.innerHTML = ""
    axios.get(`http://127.0.0.1:8000/user?mail=${emailInput.value}&password=${passwordInput.value}`).then((response) => {
        console.log(response.data);
        init_table()
        connected.innerHTML = `${emailInput.value}`
    }).catch((error) => {
        console.log(error);
        error_message.innerHTML = error.response.data.detail
    })
}


const registerButton = document.getElementById("register");

registerButton.onclick = () => {
    error_alert.innerHTML = ""
    axios.post(`http://127.0.0.1:8000/user?mail=${emailInput.value}&password=${passwordInput.value}`).then((response) => {
        console.log(response.data);
        error_alert.innerHTML = ""
        init_table()
        connected.innerHTML = `${emailInput.value}`
    }).catch((error) => {
        console.log(error);
        error_message.innerHTML = error.response.data.detail
    })
}


const currencyInput = document.getElementById("currency");
const methodInput = document.getElementById("method");
const tresholdInput = document.getElementById("treshold");

const addButton = document.getElementById("add-currency");

const deleteButton = document.getElementById("delete");


addButton.onclick = () => {
    error_alert.innerHTML = ""
    axios.post(`http://127.0.0.1:8000/alert/?mail=${emailInput.value}&password=${passwordInput.value}&currency=${currencyInput.value}&price=${tresholdInput.value}&method=${methodInput.value}`).then((response) => {
        console.log(response.data);
        appendRow(response.data.currency, response.data.method, response.data.price);
    }).catch((error) => {
        console.log(error);
        error_alert.innerHTML = error.response.data.detail
    });
}


deleteButton.onclick = () =>
{
    error_alert.innerHTML = ""
    axios.delete(`http://127.0.0.1:8000/alert/?mail=${emailInput.value}&password=${passwordInput.value}&currency=${currencyInput.value}&price=${tresholdInput.value}&method=${methodInput.value}`).then((response) => {
        console.log(response.data);
        init_table()
    }).catch((error) => {
        console.log(error);
        error_alert.innerHTML = error.response.data.detail
    })
}