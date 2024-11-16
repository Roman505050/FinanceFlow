const coinTypes = [
    {symbol: '₴', color: '#ffd700'},  // Grivna
    {symbol: '$', color: '#85bb65'},  // Dollar
    {symbol: '€', color: '#0f47af'},  // Euro
    {symbol: '£', color: '#cf9fff'},  // Pound
    {symbol: '¥', color: '#ff9999'},  // Yen
    {symbol: '₿', color: '#f7931a'},  // Bitcoin
];

function createCoin() {
    const coin = document.createElement('div');
    const coinType = coinTypes[Math.floor(Math.random() * coinTypes.length)];

    coin.classList.add('coin');
    coin.style.left = `${Math.random() * 100}vw`;
    coin.style.animationDuration = `${Math.random() * 5 + 10}s`;
    coin.textContent = coinType.symbol;
    coin.style.backgroundColor = coinType.color;

    document.body.appendChild(coin);

    setTimeout(() => {
        coin.remove();
    }, 10000);
}

setInterval(createCoin, 1000);

document.addEventListener('DOMContentLoaded', function () {
    const errorIcon = document.querySelector('.error-icon');
    errorIcon.style.transition = 'transform 0.3s ease';

    errorIcon.addEventListener('mouseover', function () {
        this.style.transform = 'scale(1.1) rotate(5deg)';
    });

    errorIcon.addEventListener('mouseout', function () {
        this.style.transform = 'scale(1) rotate(0deg)';
    });
});