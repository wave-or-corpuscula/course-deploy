
function addRow() {
    const table = document.getElementById("simplex-table");
    const numCols = table.rows[0].cells.length; // Number of columns

    if (table.rows.length <= 11) {
        const newRow = table.insertRow(table.rows.length - 1);
        const headerCell = document.createElement("th");
        headerCell.textContent = `Материал ${table.rows.length - 2}`;
        newRow.appendChild(headerCell);

        for (let i = 1; i < numCols; i++) {
            const newCell = newRow.insertCell(-1);
            const input = document.createElement("input");
            if (i != numCols - 1) {
                input.name = `cell-${table.rows.length - 2}-${i}`;
            } 
            else {
                input.name = `reserve-${table.rows.length - 2}`;
            }
            newCell.appendChild(input);
        }
    }
}

function deleteRow() {
    const table = document.getElementById("simplex-table");
    const lastRowIndex = table.rows.length - 2;
    const lastColIndex = table.rows[0].cells.length - 2;

    // Check if we have more than the header row and column
    if (lastRowIndex > 2) {
        table.deleteRow(lastRowIndex);
    }
}

function getReserves() {
    const table = document.getElementById("simplex-table");
    const reservesCount = table.rows.length - 2;

    reserves = [];
    for (let i = 0; i < reservesCount; i++) {
        reserves.push(document.getElementsByName(`reserve-${i + 1}`)[0].value);
    }
    return reserves;
}

function addColumn() {
    // Get the table and its rows
    const table = document.getElementById("simplex-table");
    const rows = table.rows;
    const reserves = getReserves();

    try {
        deleteColumn_(table.rows[0].cells.length - 1);
    }
    catch (err) {

    }
    
    // Add a new header cell at the end of the header row
    const headerRow = rows[0];
    const newHeaderCell = document.createElement("th");
    newHeaderCell.textContent = `Продукт ${headerRow.cells.length}`;
    headerRow.appendChild(newHeaderCell);

    // Add a new cell at the end of each body row
    for (let i = 1; i < rows.length; i++) {
        const newCell = document.createElement("td");
        const input = document.createElement("input");
        if (i != rows.length - 1) {
            input.name = `cell-${i}-${headerRow.cells.length - 1}`;
        }
        else {
            input.name = `profit-${headerRow.cells.length - 1}`;
        }
        newCell.appendChild(input);
        rows[i].appendChild(newCell);
    }

    addReserves(reserves);
}

function deleteColumn_(col_index) {
    const table = document.getElementById("simplex-table");

    for (let i = 0; i < table.rows.length; i++) {
        table.rows[i].deleteCell(col_index);
    }
}

function deleteColumn() {
    const table = document.getElementById("simplex-table");

    if (table.rows[0].cells.length > 4) {
        deleteColumn_(table.rows[0].cells.length - 2);
    }
}

function setInitialParameters(initTable, initRes, initProfits) {
    const table = document.getElementById("simplex-table");
    const deltaRows = initTable.length - (table.rows.length - 2);
    const deltaCols = initTable[0].length - (table.rows[0].cells.length - 2);

    
    for (let i = 0; i < deltaRows; i++) addRow();
    for (let i = 0; i < deltaCols; i++) addColumn();
    
    for (let i = 0; i < initTable.length; i++) {
        for (let j = 0; j < initTable[0].length; j++) {
            // Заполняем ячейки начальными знаениями
            const input = document.getElementsByName(`cell-${i + 1}-${j + 1}`)[0];
            input.value = initTable[i][j];

        }
        // Заполняем резервы начальными значениями
        const reserveInput = document.getElementsByName(`reserve-${i + 1}`)[0];
        reserveInput.value = initRes[i];
    }
    // Заполняем стоимости начальными значениям
    for (let i = 0; i < initProfits.length; i++) {
        const profitInput = document.getElementsByName(`profit-${i + 1}`)[0];
        profitInput.value = initProfits[i];
    }
}

// Получение данных таблицы
function getTableData() {
    const table = document.getElementById("simplex-table");

    tableData = [];
    for (let i = 0; i < table.rows.length - 2; i++) {
        const tableRow = [];
        for (let j = 0; j < table.rows[0].cells.length - 2; j++) {
            const input = document.getElementsByName(`cell-${i + 1}-${j + 1}`)[0];
            tableRow.push(input.value);
        }
        tableData.push(tableRow);
    }
    return tableData;
}

// Получение всех стоимостей с формы
function getProfits() {
    const table = document.getElementById("simplex-table");
    const profitsAmount = table.rows[0].cells.length - 2;

    prices = [];
    for (let i = 0; i < profitsAmount; i++) {
        const profit = document.getElementsByName(`profit-${i + 1}`)[0].value;
        prices.push(profit);
    }

    return prices;
}

// Получение всех резервов с формы
function addReserves(reserves) {
    // Get the table and its rows
    const table = document.getElementById("simplex-table");
    const rows = table.rows;

    // Add a new header cell at the end of the header row
    const headerRow = rows[0];
    const newHeaderCell = document.createElement("th");
    newHeaderCell.textContent = "Запасы";
    headerRow.appendChild(newHeaderCell);

    // Add a new cell at the end of each body row
    for (let i = 1; i < rows.length - 1; i++) {
        const newCell = document.createElement("td");
        const input = document.createElement("input");
        input.name = `reserve-${i}`;
        input.value = reserves[i - 1];
        newCell.appendChild(input);
        rows[i].appendChild(newCell);
    }
}

function simplexSolve() {

    const simplexAnswerDiv = document.getElementById("simplex-solution");
    const errorMessageDiv = document.getElementById("error-message");

    const formData = {
        profits: getProfits(),
        reserves: getReserves(),
        tableData: getTableData()
    }

    fetch('/simplex_solve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ formData: formData }),
        })
        .then(response => {
        if (response.ok) {
            return response.json()
        } else {
            throw new Error("Something went")
        }
        })
        .then((data) => {
        const html = data.html
        if (data.ok) {
            simplexAnswerDiv.innerHTML = html;
            errorMessageDiv.innerHTML = "";
            console.log("Data received successfuly!");
        } else {
            errorMessageDiv.innerHTML = html;
            simplexAnswerDiv.innerHTML = "";
            console.log("Error in receiveing data((");
        }
        })
        .catch(error => {
        console.error('Произошла ошибка:', error);
    });
}

function evolutionSolve() {
    const evolutionAnswerDiv = document.getElementById("evolution-solution");
    const errorMessageDiv = document.getElementById("error-message");

    const formData = {
        profits: getProfits(),
        reserves: getReserves(),
        tableData: getTableData(),
        populationSize: document.getElementById("populationSize").value,
        numGenerations: document.getElementById("numGenerations").value,
        mutationRate: document.getElementById("mutationRate").value,
        tournamentSize: document.getElementById("tournamentSize").value,
        minArgVal: document.getElementById("minArgVal").value,
        maxArgVal: document.getElementById("maxArgVal").value
    }

    evolutionAnswerDiv.innerHTML = "Идет эволюция..."

    fetch('/evolution_solve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ formData: formData }),
        })
        .then(response => {
        if (response.ok) {
            return response.json()
        } else {
            throw new Error("Something went")
        }
        })
        .then((data) => {
        const html = data.html
        if (data.ok) {
            evolutionAnswerDiv.innerHTML = html;
            errorMessageDiv.innerHTML = "";
        } else {
            errorMessageDiv.innerHTML = html;
            evolutionAnswerDiv.innerHTML = "";
        }
        })
        .catch(error => {
        console.error('Произошла ошибка:', error);
    });
}

function changeReserves() {
    try {
        const table = document.getElementById("simplex-table");
        const reservesCount = table.rows.length - 2;
        const changeValue = parseFloat(document.getElementById("reserves-change-val").value) / 100;
    
        for (let i = 0; i < reservesCount; i++) {
            const res_val = parseFloat(document.getElementsByName(`reserve-${i + 1}`)[0].value);
            const result_val = res_val + res_val * changeValue;
            if (isNaN(result_val)) {
                return;
            }
            document.getElementsByName(`reserve-${i + 1}`)[0].value = Math.round(result_val * 100) / 100;
        }
    }
    catch {
        console.log("Ecxeption occured((");
    }
}

function changeProfits() {
    try {
        const table = document.getElementById("simplex-table");
        const profitsAmount = table.rows[0].cells.length - 2;
        const changeValue = parseFloat(document.getElementById("profits-change-val").value) / 100;
    
        for (let i = 0; i < profitsAmount; i++) {
            const profit = parseFloat(document.getElementsByName(`profit-${i + 1}`)[0].value);
            const new_profit = profit + profit * changeValue;
            if (isNaN(new_profit)) {
                return;
            }
            document.getElementsByName(`profit-${i + 1}`)[0].value = Math.round(new_profit * 100) / 100;
        }
    
    }
    catch {
        console.log("Ecxeption occured((");
    }
    
}



document.addEventListener("DOMContentLoaded", function() {

    const initialTable = [
        [0.8, 0.5, 1, 2, 1.1],
        [0.2, 0.1, 0.1, 0.1, 0.2],
        [0.3, 0.4, 0.6, 1.3, 0.05],
        [0.2, 0.3, 0.3, 0.7, 0.5],
        [0.7, 0.1, 0.9, 1.5, 0]
    ];
    const initialReserves = [1411, 149, 815.5, 466, 1080];
    const initialProfits = [1, 0.7, 1, 2, 0.6];

    document.getElementById("add-row").addEventListener("click", addRow);
    document.getElementById("delete-row").addEventListener("click", deleteRow);
    document.getElementById("add-column").addEventListener("click", addColumn);
    document.getElementById("delete-column").addEventListener("click", deleteColumn);

    document.getElementById("simplex-solve").addEventListener("click", simplexSolve);
    document.getElementById("evolutionary-solve").addEventListener("click", evolutionSolve);

    document.getElementById("change-reserves").addEventListener("click", changeReserves);
    document.getElementById("change-profits").addEventListener("click", changeProfits);

    setInitialParameters(initialTable, initialReserves, initialProfits);
});