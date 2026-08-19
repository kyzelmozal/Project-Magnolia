async function getStockInfo() {
    const ticker = document.getElementById("tickerInput").value;
    const response = await fetch(`/api/stock/${ticker}`);
    const data = await response.json();

    console.log(data);
}

async function getStockMargins() {
    const ticker = document.getElementById("tickerInput").value;
    const response = await fetch(`/api/margins/${ticker}`);
    const data = await response.json();

    console.log(data);
}