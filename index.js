const totalImages = 3; // Aantal afbeeldingen (handmatig in te voeren)
let slideIndex = 1; // Beginindex

if (window.innerWidth < 768) {
    alert("Waarwschuwing! Deze website is niet gemaakt voor een Telefoon of een Tablat. Je kunt de website beter bekijken op een PC");
}

showDivs(slideIndex);

// Interval om automatisch de afbeeldingen te veranderen
setInterval(() => {
    plusDivs(1); // Verander naar de volgende afbeelding
}, 5000); // 10000 milliseconden = 10 seconden

function plusDivs(n) {
    showDivs(slideIndex += n);
}

function showDivs(n) {
    let i;
    let x = document.getElementsByClassName("image");
    // Zorg ervoor dat slideIndex binnen de juiste grenzen blijft
    if (n > totalImages) { slideIndex = 1; }
    if (n < 1) { slideIndex = totalImages; }

    // Verberg de huidige afbeelding en verwijder de 'show' klasse
    for (i = 0; i < x.length; i++) {
        x[i].classList.remove('show'); // Verberg alle afbeeldingen
    }
    // Toon de juiste afbeelding en voeg de 'show' klasse toe
    x[slideIndex - 1].classList.add('show'); // Toon de juiste afbeelding
}
