console.log("JavaScript is working!");
fetch("website/results.json")
    .then(response => response.json())
    .then(dcfData => {
        const tableBody = document.getElementById("dcfTable");
        
        dcfData.forEach(item => {

            tableBody.innerHTML += `
                <tr>
                    <td>${item.ticker}</td>
                    <td>${item.futurePrice}</td>
                    <td>${item.currentPrice}</td>
                    <td>${item.upside}</td>
                </tr>
            `;
    })
});
console.log("Data fetched and table populated!");