$(function() {
    var positionError = false;
    $("#id_position").autocomplete({
        source: positionAutocompleteUrl, // Використовуємо глобальну змінну для URL
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
            },
        select: function(event, ui) {
            // Завантаження категорій тут
            $.ajax({
                url: getCategoriesUrl, // Використовуємо глобальну змінну для URL
                data: {
                    position: ui.item.value
                },
                success: function(data) {
                    var categoryList = $('#category_list');
                    categoryList.empty();
                    $.each(data, function(index, category) {
                        var categoryBlock = `
                            <div class="type-category">
                                <p class="category-name">${category}</p>
                            </div>`;
                        categoryList.append(categoryBlock);
                    });
                }
            });
        }
    });
    $("#id_position").on("focusout", function() {
        var positionName = $(this).val();

        $.ajax({
            url: positionAutocompleteUrl,
            data: { term: positionName },
            success: function(data) {
                if (data.length === 0) {
                    $("#id_position").addClass("error-border");
                    $("#position-error-message").show();
                    positionError = true;  // Встановлюємо прапорець
                } else {
                    $("#id_position").removeClass("error-border");
                    $("#position-error-message").hide();
                    positionError = false;  // Скидаємо прапорець
                }
            }
        });
    });
});
