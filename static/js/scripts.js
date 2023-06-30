
    window.addEventListener("scroll", function() {
        var footer = document.getElementById("footer");
        var footerHiddenClass = "footer-hidden";
        var footerClass = "footer"

        var windowHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

        var documentHeight = Math.max(
            document.body.scrollHeight,
            document.documentElement.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.offsetHeight,
            document.body.clientHeight,
            document.documentElement.clientHeight
        );

        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;

        if (windowHeight + scrollTop >= documentHeight) {
            if (footer.classList.contains(footerHiddenClass)) {
                footer.classList.remove(footerHiddenClass);
            }
            footer.classList.add(footerClass);
        } else {
            if (footer.classList.contains(footerClass)) {
                footer.classList.remove(footerClass);
            }
            footer.classList.add(footerHiddenClass);
        }
    });



