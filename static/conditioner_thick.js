//buy_conditioner_thick.js
document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('buy_conditioner_thick_button');

    button.addEventListener('click', () => {
        // Set the desired Amazon link to open in a new tab when the button is clicked
        const link = "https://www.amazon.com/Garnier-Fructis-Nutrition-Moisture-Conditioner/dp/B078PLG6MM/ref=sr_1_3?crid=19RZQ89J1E5WE&keywords=thick+leave+in+conditioner+for+curly+hair&qid=1695501518&s=books&sprefix=thick+leave+in+cond%2Cstripbooks%2C78&sr=1-3";
        window.open(link, '_blank');
    });
});
