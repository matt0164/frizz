//buy_book_button.js
document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('buy_book_button');

    button.addEventListener('click', () => {
        // Set the desired Amazon link to open in a new tab when the button is clicked
        const link = "https://www.amazon.com/Curly-Girl-Handbook-Michele-Bender/dp/076115678X";
        window.open(link, '_blank');
    });
});
