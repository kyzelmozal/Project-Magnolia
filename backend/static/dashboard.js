async function getStockInfo() {
    const ticker = document.getElementById("tickerInput").value;
    const response = await fetch(`/api/stock/${ticker}`);
    const data = await response.json();

    console.log(data);
}