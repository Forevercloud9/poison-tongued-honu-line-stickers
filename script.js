document.addEventListener('DOMContentLoaded', () => {
    const quotes = [
        "......なに見てんの？",
        "善処します(しない)",
        "はいはい、聞いてるよ",
        "そのうちやるってば",
        "聞こえてるよ、無視してるだけ",
        "マジで言ってる？",
        "了解（逃走）",
        "呼んだ？呼んでない？ふーん",
        "生きてるだけで偉いでしょ",
        "暇なの？私は忙しいけど",
        "もう寝るわ、永遠に",
        "で？オチは？",
        "貸しイチな、利子は高いよ",
        "見直した（嘘）",
        "褒めてつかわす、光栄に思え",
        "期待以上、珍しくね",
        "これでチャラな、感謝しろよ",
        "知らんがな、自分で考えろ",
        "パスで、めんどくさい",
        "現実逃避中、話しかけんな",
        "どうでもいい、宇宙規模で",
        "カメなんで遅れます、文句ある？",
        "ムリ、絶対ムリ",
        "噴火5秒前、逃げれば？",
        "手が滑った...あっ（棒）",
        "……あ？聞こえん",
        "仏の顔も終了、地獄行き",
        "無かったことに、記憶消去",
        "帰っていい？今すぐ",
        "詰んだ、終わった",
        "先が見えない、暗闇",
        "終わったわ、何もかも",
        "名案（悪だくみ）",
        "その手があったか、悪知恵",
        "天才私、ひれ伏せ",
        "解決してないけど、まいいか",
        "正気か？病院行く？",
        "開いた口が塞がらんわ",
        "へーすごいね（棒読み）"
    ];

    const quoteElement = document.getElementById('randomQuote');
    const pokeButton = document.getElementById('pokeButton');
    const heroImage = document.querySelector('.main-visual');

    // Function to get a random quote
    function getRandomQuote() {
        const randomIndex = Math.floor(Math.random() * quotes.length);
        return quotes[randomIndex];
    }

    // Event listener for the button
    pokeButton.addEventListener('click', () => {
        // Change text
        const newQuote = getRandomQuote();
        quoteElement.style.opacity = 0;
        
        setTimeout(() => {
            quoteElement.textContent = newQuote;
            quoteElement.style.opacity = 1;
        }, 200);

        // Animate image a bit
        heroImage.style.transform = "scale(1.1) rotate(5deg)";
        setTimeout(() => {
            heroImage.style.transform = "scale(1) rotate(0deg)";
        }, 200);
    });

    // Add CSS transition for opacity
    quoteElement.style.transition = "opacity 0.2s ease-in-out";
});
