$(document).ready(function () {
    const successMessage = $("#jq-notification");
    const CartCounters = $(".goods-in-cart-count");
    const cartItemsContainer = $(".basket_items");

    // Универсальная функция обновления интерфейса корзины
    function updateCartUI(data, isAdd = null) {
        // Показываем уведомление
        successMessage.html(data.message).fadeIn(400);

        // Очищаем предыдущие таймеры
        setTimeout(() => successMessage.fadeOut(400), 5000);

        // Обновляем счетчик
        let currentCount = parseInt($CartCounters.first().text() || 0);
        let totalCount = data.total_quantity;

        if (totalCount !== undefined) {
            $cartCounters.text(totalCount);
        } else if (isAdd === true) {
            $cartCounters.text(currentCount + 1);
        } else if (isAdd === false && data.quantity_deleted !== undefined) {
            $cartCounters.text(currentCount - data.quantity_deleted);
        }

        // Перерисовываем корзину
        if (data.cart_items_html) {
            cartItemsContainer.html(data.cart_items_html);
        }
    }

    // Обработка уведомлений от Django (messages)
    const notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(() => notification.alert('close'), 5000);
    }

    // Делегирование событий для корзины (объединяем логику)
    $(document).on("click", ".add-to-cart, .remove-from-cart", function (e) {
        e.preventDefault();
        const $el = $(this);
        const url = $el.attr("href");
        const isAdding = $el.hasClass("add-to-cart");

        const postData = {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        };

        if (isAdding) {
            postData.product_id = $el.data("product-id");
        } else {
            postData.cart_id = $el.data("cart-id");
        }

        $.ajax({
            type: "POST",
            url: url,
            cache: false,
            data: postData,
            success: function(data) {
                updateCartUI(data, isAdding);
            },
            error: () => console.error("Ошибка при обновлении корзины")
        });
    });

    // Изменение количества
    $(document).on("change input", ".cart-change", function () {
        const $el = $(this);
        $.ajax({
            type: "POST",
            url: $el.data('cart-change-url'),
            cache: false,
            data: {
                cart_id: $el.data('cart-id'),
                quantity: $el.val(),
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: updateCartUI,
            error: () => console.error("Ошибка при изменении количества")
        });
    });

    // Доставка
    $("input[name='requires_delivery']").on("change", function () {
        $("#deliveryAddressField").toggle($(this).val() === "1");
    });

    // Маска телефона (с защитой от null)
    const phoneInput = document.getElementById('id_phone_number');
    if (phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            let x = e.target.value.replace(/\D/g, '')
                    .match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
            // Если нет второй группы цифр, пишем только первую,
            // иначе добавляем скобки
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' +
            x[2] + (x[3] ? '-' + x[3] : '');
        });
    }

    // Валидация формы заказа
    $('#create_order_form').on('submit', function (e) {
        const $phone = $('#id_phone_number');
        const phoneNumber = $phone.val();
        const regex = /^\(\d{3}\) \d{3}-\d{4}$/;

        if (!regex.test(phoneNumber)) {
            $('#phone_number_error').show();
            e.preventDefault();
        } else {
            $('#phone_number_error').hide();
            // Очищаем перед отправкой (чтобы в базу летело 1234567890)
            $phone.val(phoneNumber.replace(/\D/g, ''));
        }
    });
});
