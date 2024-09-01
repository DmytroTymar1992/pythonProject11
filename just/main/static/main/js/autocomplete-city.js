$(function() {
    var cityError = false;

    $("#id_city").autocomplete({
        source: cityAutocompleteUrl, // Використовуємо глобальну змінну для URL
        minLength: 2,
        appendTo: '.form__input-list-wrapper',
        open: function(event, ui) {
            var $input = $(event.target),
                $wrapper = $input.closest('.js_open'),
                wrapperWidth = $wrapper.outerWidth();

            $input.autocomplete("widget").css('width', wrapperWidth + 'px');
        },
        classes: {
            "ui-autocomplete": "search-location__select-list",
            "ui-menu-item": "search-location__select-item"
        }
    });

    // Підсвітка червоним кольором неправильно введеного міста
    $("#id_city").on("focusout", function() {
        var cityName = $(this).val();

        $.ajax({
            url: cityAutocompleteUrl,
            data: { term: cityName },
            success: function(data) {
                if (data.length === 0) {
                    $("#id_city").addClass("error-border");
                    $("#city-error-message").show();
                    cityError = true;  // Встановлюємо прапорець
                } else {
                    $("#id_city").removeClass("error-border");
                    $("#city-error-message").hide();
                    cityError = false;  // Скидаємо прапорець
                }
            }
        });
    });
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
