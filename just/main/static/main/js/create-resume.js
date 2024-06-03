$(document).ready(function() {
    console.log('Document is ready');
    // Функції для додавання форм
    $('#add-education').click(function(e){
        e.preventDefault();
        var form_idx = $('#id_education_set-TOTAL_FORMS').val();
        var newForm = $('#empty-education-form').html().replace(/__prefix__/g, form_idx);
        $('#educations-formset').append(newForm);
        $('#id_education_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        addDeleteButton('.education-form');
    });

    $('#add-work-experience').click(function(e){
        e.preventDefault();
        var form_idx = $('#id_workexperience_set-TOTAL_FORMS').val();
        var newForm = $('#empty-work-experience-form').html().replace(/__prefix__/g, form_idx);
        $('#work-experiences-formset').append(newForm);
        $('#id_workexperience_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        addDeleteButton('.work-experience-form');
    });

    $('#add-course').click(function(e){
        e.preventDefault();
        var form_idx = $('#id_course_set-TOTAL_FORMS').val();
        var newForm = $('#empty-course-form').html().replace(/__prefix__/g, form_idx);
        $('#courses-formset').append(newForm);
        $('#id_course_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        addDeleteButton('.course-form');
    });

    $('#add-user-language').click(function(e){
        e.preventDefault();
        var form_idx = $('#id_userlanguage_set-TOTAL_FORMS').val();
        var newForm = $('#empty-user-language-form').html().replace(/__prefix__/g, form_idx);
        $('#user-languages-formset').append(newForm);
        $('#id_userlanguage_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        addDeleteButton('.user-language-form');
    });

    function addDeleteButton(formClass) {
        $(formClass).each(function() {
            if (!$(this).find('.delete-form').length) {
                $(this).append('<button type="button" class="delete-form">Видалити</button>');
            }
        });
    }

    $(document).on('click', '.delete-form', function(e){
        e.preventDefault();
        $(this).closest('.form-row').remove();
        updateTotalForms();
    });

    function updateTotalForms() {
        var educationTotalForms = $('.education-form').length;
        $('#id_education_set-TOTAL_FORMS').val(educationTotalForms);

        var workExperienceTotalForms = $('.work-experience-form').length;
        $('#id_workexperience_set-TOTAL_FORMS').val(workExperienceTotalForms);

        var courseTotalForms = $('.course-form').length;
        $('#id_course_set-TOTAL_FORMS').val(courseTotalForms);

        var userLanguageTotalForms = $('.user-language-form').length;
        $('#id_userlanguage_set-TOTAL_FORMS').val(userLanguageTotalForms);
    }

    addDeleteButton('.education-form');
    addDeleteButton('.work-experience-form');
    addDeleteButton('.course-form');
    addDeleteButton('.user-language-form');



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
                    url: "{% url 'create_resume' %}",
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



