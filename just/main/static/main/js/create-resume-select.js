$(document).ready(function() {
    function split(val) {
        return val.split(/,\s*/);
    }

    function extractLast(term) {
        return split(term).pop();
    }

    $('#id_desired_positions').on('keydown', function(event) {
        if (event.keyCode === $.ui.keyCode.TAB && $(this).autocomplete('instance').menu.active) {
            event.preventDefault();
        }
    }).autocomplete({
        source: function(request, response) {
            $.ajax({
                url: createResumeUrl,
                dataType: "json",
                data: {
                    term: extractLast(request.term)
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        search: function() {
            var term = extractLast(this.value);
            if (term.length < 2) {
                return false;
            }
        },
        focus: function() {
            return false;
        },
        select: function(event, ui) {
            var terms = split(this.value);
            terms.pop();
            terms.push(ui.item.value);
            terms.push('');
            this.value = terms.join(', ');
            return false;
        }
    });
});