
    window.addEventListener("scroll", function() {
        var footer = document.getElementById("footer");
        var footerHiddenClass = "footer-hidden";
        var footerClass = "footer"

        // Calcola l'altezza della finestra visualizzabile
        var windowHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

        // Calcola l'altezza totale della pagina
        var documentHeight = Math.max(
            document.body.scrollHeight,
            document.documentElement.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.offsetHeight,
            document.body.clientHeight,
            document.documentElement.clientHeight
        );

        // Calcola la posizione verticale corrente dello scroll
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;

        // Verifica se si è arrivati alla fine della pagina
        if (windowHeight + scrollTop >= documentHeight) {
            // Rimuovi la classe di nascondere il footer
            if (footer.classList.contains(footerHiddenClass)) {
                footer.classList.remove(footerHiddenClass);
            }
            footer.classList.add(footerClass);
        } else {
            // Aggiungi la classe per nascondere il footer
            if (footer.classList.contains(footerClass)) {
                footer.classList.remove(footerClass);
            }
            footer.classList.add(footerHiddenClass);
        }
    });



