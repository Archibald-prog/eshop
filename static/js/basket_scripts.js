$(document).ready(function () {
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Меняем значение счетчика
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Перерисовываем html-код с разметкой корзины
                var cartItemsContainer = $(".basket_items");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                var cartItemsContainer = $(".basket_items");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при удалении товара из корзины");
            },
        });
    });

    $(document).on("click", ".cart-change", function (e) {
        var target_href = event.target;
        var url = target_href.getAttribute('data-cart-change-url');
        var cartID = target_href.getAttribute('data-cart-id');
        var currentValue = target_href.value;

        $.ajax({
           type: "POST",
           url: url,
           data: {
               cart_id: cartID,
               quantity: currentValue,
               csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
           },
           success: function (data) {
               var goodsInCartCount = $("#goods-in-cart-count");
               var cartCount = parseInt(goodsInCartCount.text() || 0);

               cartCount = data.total_quantity;
               goodsInCartCount.text(cartCount);

               var cartItemsContainer = $(".basket_items");
               cartItemsContainer.html(data.cart_items_html);

           },
           error: function (data) {
               console.log("Ошибка при изменении количества товара");
           },
        });
    });

});

