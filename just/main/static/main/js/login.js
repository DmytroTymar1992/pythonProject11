document.addEventListener('DOMContentLoaded', function () {
    const submitBtn = document.getElementById('submitBtn');
    const searchBtn = document.getElementById('searchBtn');
    const employerBtn = document.getElementById('employerBtn');
    const searcherForm = document.getElementById('searcherForm');
    const employerForm = document.getElementById('employerForm');

    submitBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (searchBtn.classList.contains('user__actions-modal-active')) {
            searcherForm.submit();
        } else if (employerBtn.classList.contains('user__actions-modal-active')) {
            employerForm.submit();
        }
    });
});
