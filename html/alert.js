const table = document.getElementById("table-content");
const error_message = document.getElementById("error_message");
const error_alert = document.getElementById("error_alert")

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
    axios.get(`http://37.187.55.169:8000/alert?mail=${emailInput.value}`).then((response) => {
        console.log(response.data);
        response.data.forEach((element) => {
            appendRow(element.currency, element.method, element.price);
        })

    }).catch((error) => {
        console.log(error);
    })   
}

loginButton.onclick = () => {
    axios.get(`http://37.187.55.169:8001/user?mail=${emailInput.value}&password=${passwordInput.value}`).then((response) => {
        console.log(response.data);
        init_table()
    }).catch((error) => {
        console.log(error);
        error_message.innerHTML = error.response.data.detail
    })
}


const registerButton = document.getElementById("register");

registerButton.onclick = () => {
    axios.post(`http://37.187.55.169:8001/user?mail=${emailInput.value}&password=${passwordInput.value}`).then((response) => {
        console.log(response.data);
        init_table()
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
    axios.post(`http://37.187.55.169:8000/alert/?mail=${emailInput.value}&currency=${currencyInput.value}&price=${tresholdInput.value}&method=${methodInput.value}`).then((response) => {
        console.log(response.data);
        error_alert.innerHTML = ""
        appendRow(response.data.currency, response.data.method, response.data.price);
    }).catch((error) => {
        console.log(error);
        error_alert.innerHTML = error.response.data.detail
    });
}


deleteButton.onclick = () =>
{
    table.remove()
    error_alert.innerHTML = ""
    axios.delete(`http://37.187.55.169:8000/all_alert?mail=${emailInput.value}`).then((response) => {
        console.log(response.data);
    }).catch((error) => {
        console.log(error);
        error_alert.innerHTML = error.response.data.detail
    })
}