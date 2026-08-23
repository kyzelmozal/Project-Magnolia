
const goButton = document.getElementById("goButton");
goButton.addEventListener("click", () => {
    getStockInfo();
    getStockMargins();
    getStockDCF();
    getStockEPS();
})

document.getElementById("tickerInput").addEventListener("keydown", function(event){
    if (event.key === "Enter") {
        getStockInfo();
        getStockMargins();
        getStockDCF();
        getStockEPS();
    }
});

async function getStockInfo() {
    const ticker = document.getElementById("tickerInput").value;
    const response = await fetch(`/api/stock/${ticker}`);
    const data = await response.json();

    data.price = +data.price.toFixed(2)
    document.getElementById("currentPrice").innerText = "Price: " + data.price;

    console.log(data);
}

async function getStockEPS() {
    const ticker = document.getElementById("tickerInput").value;
    const response = await fetch(`/api/EPS/${ticker}`);
    const data = await response.json();
    
    lastQuarterEPSGrowth = +data.lastQuarterEPSGrowth.toFixed(1);
    lastYearEPSGrowth = +data.lastYearEPSGrowth.toFixed(1);
    last3YearEPSGrowth = +data.last3YearEPSGrowth.toFixed(1);

    document.getElementById("lastQuarterEPSGrowth").innerText = `Last Quarter EPS Growth: ${lastQuarterEPSGrowth}%`
    document.getElementById("lastYearEPSGrowth").innerText = `Last Year EPS Growth: ${lastYearEPSGrowth}%`
    document.getElementById("last3YearEPSGrowth").innerText = `Last 3 Years EPS Growth: ${last3YearEPSGrowth}%`
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
    data.futurePrice3Y = +data.futurePrice3Y.toFixed(2);
    data.upside1Y = +data.upside1Y.toFixed(1);
    data.upside3Y = +data.upside3Y.toFixed(1);
    document.getElementById("1YPrice").innerText = `Price in 1Y: ${data.futurePrice1Y} ${data.upside1Y}%`;
    document.getElementById("3YPrice").innerText = `Price in 3Y: ${data.futurePrice3Y} ${data.upside3Y}%`;

    console.log(data);
}