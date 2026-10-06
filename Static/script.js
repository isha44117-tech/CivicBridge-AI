console.log("CivicBridge JavaScript loaded!");
const analyzeButton = document.querySelector("button");

analyzeButton.addEventListener("click", async function () {

    const description = document.querySelector("#description").value;
    const location = document.querySelector("#location").value;
    const category = document.querySelector("#category").value;

    const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            description: description,
            location: location,
            category: category
        })
    });

    const result = await response.json();

    console.log(result);

    document.querySelector("#result").style.display = "block";

document.querySelector("#resultCategory").textContent = result.category;
document.querySelector("#resultPriority").textContent = "Pending AI";
document.querySelector("#resultSummary").textContent = result.description;
document.querySelector("#resultAuthority").textContent = "Pending AI";
});