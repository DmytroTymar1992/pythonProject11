document.addEventListener('DOMContentLoaded', function () {
    var avatarInput = document.getElementById('avatar-input');
    var avatarPreview = document.getElementById('avatar-preview');
    var cropModal = document.getElementById('cropModal');
    var cropperImage = document.getElementById('cropper-image');
    var cropAndUploadButton = document.getElementById('cropAndUploadButton');
    var croppedAvatarInput = document.getElementById('cropped-avatar');
    var cropper;
    var closeModal = document.getElementById('closeModal'); // змінено для використання id

    avatarInput.addEventListener('change', function (event) {
        var files = event.target.files;
        var done = function (url) {
            avatarInput.value = '';
            cropperImage.src = url;
            cropModal.style.display = 'flex';
            if (cropper) {
                cropper.destroy();
            }
            cropper = new Cropper(cropperImage, {
                aspectRatio: 1,
                viewMode: 1,
                autoCropArea: 1,
                responsive: true,
            });
        };
        var reader;
        var file;
        var url;

        if (files && files.length > 0) {
            file = files[0];

            if (URL) {
                done(URL.createObjectURL(file));
            } else if (FileReader) {
                reader = new FileReader();
                reader.onload = function (event) {
                    done(event.target.result);
                };
                reader.readAsDataURL(file);
            }
        }
    });

    closeModal.onclick = function () {
        cropModal.style.display = 'none';
        if (cropper) {
            cropper.destroy();
            cropper = null;
        }
    };

    cropAndUploadButton.addEventListener('click', function () {
        var canvas;
        if (cropper) {
            canvas = cropper.getCroppedCanvas({
                width: 300,
                height: 300,
            });
            canvas.toBlob(function (blob) {
                var reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = function () {
                    var base64data = reader.result;
                    avatarPreview.src = base64data;
                    croppedAvatarInput.value = base64data; // Збереження обрізаного зображення у прихованому полі
                    cropModal.style.display = 'none';
                    cropper.destroy();
                    cropper = null;
                };
            });
        }
    });
});
