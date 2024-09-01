$(document).ready(function(){
    $('#id_city_name').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "{% url 'get_city_suggestions' %}",
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item.name,
                            value: item.name,
                            id: item.id
                        };
                    }));
                }
            });
        },
        minLength: 2,
        select: function(event, ui) {
            $('#id_city_name').val(ui.item.value);
            $('#id_city_id').val(ui.item.id);
            $('#city_not_found').hide();
        },
        change: function(event, ui) {
            if (!ui.item) {
                $('#id_city_id').val('');
            }
        },
        response: function(event, ui) {
            if (ui.content.length === 0) {
                $('#city_not_found').show();
            } else {
                $('#city_not_found').hide();
            }
        },
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
        appendTo: '.form__input-wrapper_city'
    });

    $('#id_city_name').on('blur', function() {
        var cityName = $(this).val();
        if (cityName) {
            $.ajax({
                url: "{% url 'get_city_suggestions' %}",
                dataType: "json",
                data: {
                    term: cityName
                },
                success: function(data) {
                    var cityFound = false;
                    $.each(data, function(index, item) {
                        if (item.name.toLowerCase() === cityName.toLowerCase()) {
                            $('#id_city_id').val(item.id);
                            cityFound = true;
                            $('#city_not_found').hide();
                            return false;
                        }
                    });
                    if (!cityFound) {
                        $('#city_not_found').show();
                        $('#id_city_id').val('');
                    }
                }
            });
        }
    });
});
