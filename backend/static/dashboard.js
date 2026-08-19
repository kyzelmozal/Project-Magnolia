
const goButton = document.getElementById("goButton");
goButton.addEventListener("click", () => {
    getStockInfo();
    getStockMargins();
    getStockDCF();
})

document.getElementById("tickerInput").addEventListener("keydown", function(event){
    if (event.key === "Enter") {
        getStockInfo();
        getStockMargins();
        getStockDCF();
    }
});

async function getStockInfo() {
    const ticker = document.getElementById("tickerInput").value;
    const response = await fetch(`/api/stock/${ticker}`);
    const data = await response.json();

    data.price = +data.price.toFixed(2)
    document.getElementById("priceContainer").innerText = "Price " + data.price;

    console.log(data);
}

async function getStockMargins() {
    const ticker = document.getElementById("tickerInput").value;
    const response = await fetch(`/api/margins/${ticker}`);
    const data = await response.json();

    console.log(data);
}

async function getStockDCF() {
    const ticker = document.getElementById("tickerInput").value;
    const response = await fetch(`/api/DCF/${ticker}`);
    const data = await response.json();

    data.futurePrice1Y = +data.futurePrice1Y.toFixed(2);
    document.getElementById("futurepriceContainer").innerText = "Price in 1 Year: " + data.futurePrice1Y;
    
    console.log(data);
}