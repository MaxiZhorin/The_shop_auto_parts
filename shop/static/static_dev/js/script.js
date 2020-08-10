$(document).ready(function () {
    var form = $('#form_buying_product');
    console.log(form);

    function basketUpdating(product_id, nmb, is_delete) {
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        var csrf_token = $('#csrf-token [name="csrfmiddlewaretoken"]').val();
        data['csrfmiddlewaretoken'] = csrf_token;
        var url = $('#form_buying_product').attr('action')
        console.log(csrf_token);
        if (is_delete) {
            data["is_delete"] = true;
        }

        console.log(data);

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK");
                console.log(data.products.product_id);
                if (data.products_total_nmb || data.products_total_nmb == 0) {
                    $('#basket_total_nmb').text('(' + data.products_total_nmb + ')');
                    console.log(data.products);
                    $('.basket-item ul').html("");
                    $.each(data.products, function (k, v) {
                        $('.basket-item ul').append('<li>' + v.name + ', ' + v.nmb + 'шт. *' + v.price_per_item + '₽  ' +
                            '<a class="delete-item" data-product_id="'+v.id+'" href="">X</a> ' + '' +
                            '</li>')
                        location.reload();


                    })
                }


            },
            error: function () {
                console.log("error")
            }
        });

    }

    $('.basket-container').mouseover(function (e) {
        // $("p").show("slow");
        // $('.basket-item').show("slow");
        $('.basket-item').removeAttr('style')

    });

    $('.basket-item').mouseout(function () {
        $('.basket-item').css('display','none')
    });

    $('#dropdown05').mouseover(function () {
        $('.categories').removeAttr('style')
    });

    $('.dropdown-menu show').mouseout(function () {
        $('.categories').css('display','none')
    });

    $(document).on('click','.delete-item', function (e) {
        e.preventDefault();
        product_id = $(this).data('product_id');
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete = true)
        location.reload();


    })



    $(document).on('click','.add-basket button', function (e) {
        e.preventDefault();
        product_id =$(this).data('product_id');
        var nmb = $('#number').val();
        // nmb=1;
        basketUpdating(product_id, nmb, is_delete=false)

    });

    function calculatingBasketAmount(){
        var total_order_amount = 0;
        console.log('calculating ok')
        $('.total-product-in-basket-amount').each(function() {
            total_order_amount = total_order_amount + parseFloat($(this).text());
        });
        console.log(total_order_amount,'lalalalalalalalalalala');
        $('.total_order_amountt').text(total_order_amount.toFixed(2));
    };

    $(document).on('change', ".product-in-basket-nmb", function(){
        var current_nmb = $(this).val();
        console.log(current_nmb);

        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        console.log(current_price);
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2);
        console.log(total_amount);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);

        calculatingBasketAmount();
    });

    $(document).on('click','.radio000', function (e) {
        // e.preventDefault();
        total_order_amount_radio=$(this).val();
        console.log('radio',total_order_amount_radio);
        // $(this).attr("class","total-product-in-basket-amount")
        // calculatingBasketAmount();
        $('#total_ship').empty()
        $('#total_ship').append(total_order_amount_radio)
        calculatingBasketAmount();
        console.log('lalalalaalala')
        //     + total_order_amount_radio + '</span>');


    });



    calculatingBasketAmount();

})








