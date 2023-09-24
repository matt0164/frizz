//conditioner_fine.js
document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('buy_conditioner_fine_button');

    button.addEventListener('click', () => {
        // Set the desired Amazon link to open in a new tab when the button is clicked
        const link = "https://www.amazon.com/Marc-Anthony-Leave-In-Conditioner-Detangler-Spray/dp/B076FHJ3K5/ref=sr_1_1?crid=343G2YM9UDTFP&keywords=leave+in+conditioner+fine+hair&qid=1695501642&s=books&sprefix=leave+in+conditioner+for+fine+hair%2Cstripbooks%2C84&sr=1-1-catcorr";
        window.open(link, '_blank');
    });
});
