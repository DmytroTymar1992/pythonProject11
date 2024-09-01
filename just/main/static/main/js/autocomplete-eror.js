$(function() {
    $(".vacancy-form").on("submit", function(event) {
        var hasError = false;  // Прапорець для перевірки наявності помилок

        if (cityError) {
            event.preventDefault(); // Зупиняємо відправку форми
            $("html, body").animate({
                scrollTop: $("#id_city").offset().top - 20
            }, 500);
            hasError = true;
        }

        if (positionError) {
            event.preventDefault(); // Зупиняємо відправку форми
            if (!hasError) {  // Перевіряємо, чи вже є помилка, щоб не дублювати прокрутку
                $("html, body").animate({
                    scrollTop: $("#id_position").offset().top - 20
                }, 500);
            }
            hasError = true;
        }

        // Якщо є хоча б одна помилка, форма не відправляється
        if (hasError) {
            event.preventDefault();
        }
    });
});