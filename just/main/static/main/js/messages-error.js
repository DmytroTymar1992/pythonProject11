$(document).ready(function(){
    // Function to display Toastify notifications
    function showCToast(type, message) {
        const colorMap = {
            "info": '#63B3ED',
            "success": '#2dce89',
            "error": '#f5365c',
            "default": "#20c997"
        };

        const color = colorMap[type] || colorMap["default"];

        // Configure and display the toast notification
        Toastify({
            text: message,
            duration: 3000,
            className: type,
            close: true,
            gravity: "top",
            position: "right",
            stopOnFocus: true,
            style: {
                background: color,
            },
            escapeMarkup: false,
        }).showToast();
    }

    // Extract Django messages and display them using Toastify
    const customMessages = [
        {% for message in messages %}
            {
                "tags": "{{ message.tags|default:''|escapejs }}",
                "message": '{{ message.message|default:''|escapejs }}'
            }{% if not forloop.last %},{% endif %}
        {% endfor %}
    ];

    // Debugging: Log messages to the console
    console.log(customMessages);

    // Display each custom message using Toastify
    customMessages.forEach(message => {
        showCToast(message.tags, message.message);
    });
});
