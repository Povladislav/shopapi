(function($) {
    $(document).ready(function() {
        // Находим кнопку "Копировать Email"
        var copyEmailButton = $('<a class="button" style="margin-left: 5px;">Копировать Email</a>');

        // Добавляем кнопку к элементу с ID "content-main"
        $('#content-main').find('.submit-row').append(copyEmailButton);

        // Добавляем обработчик события для кнопки
        copyEmailButton.on('click', function() {
            // Находим значение электронной почты и копируем его в буфер обмена
            var email = $('.field-email').text().trim();
            if (email) {
                // Создаем временный элемент input для копирования текста
                var tempInput = $('<input>');
                $('body').append(tempInput);
                tempInput.val(email).select();
                document.execCommand('copy');
                tempInput.remove();

                // Оповещение об успешном копировании
                alert('Email скопирован в буфер обмена: ' + email);
            }
        });
    });
})(django.jQuery);
