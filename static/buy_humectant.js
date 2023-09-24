//buy_humectant.js
document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('buy_humectant_button');

    button.addEventListener('click', () => {
        // Set the desired Amazon link to open in a new tab when the button is clicked
        const link = "https://www.amazon.com/Aveda-Brilliant-Pommade-Humectant-Ounce/dp/B001ORCEMA/ref=sr_1_1?crid=3UTANESPO8ZDC&keywords=film+forming+humectant&qid=1695501026&s=books&sprefix=film+forming+hu%2Cstripbooks%2C67&sr=1-1";
        window.open(link, '_blank');
    });
});
