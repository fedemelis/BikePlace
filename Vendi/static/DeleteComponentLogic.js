
document.addEventListener('DOMContentLoaded', function () {
    var deleteButtons = document.querySelectorAll('[id^="deleteButton-"]');
    deleteButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            var response = confirm("Sei sicuro di voler eliminare il componente?");
            var pk = button.getAttribute("data-pk");
            var url = "{% url 'Vendi:delete_component' 0 %}";
            var finalUrl = url.replace("0", pk);
            if (response === true) {
                let xhr = new XMLHttpRequest();
                xhr.open("POST", finalUrl, true);
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");

                xhr.onload = function () {
                    if (this.status >= 200 && this.status < 300) {
                        window.location.href = "{% url 'Vendi:list_components' %}";
                    } else {
                        alert("Errore: " + xhr.responseText);
                    }
                };
                xhr.send();
            }
        });
    });
});
