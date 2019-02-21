//Set CSRF Tokken into AJAX Request ////////////////////////////////////////////////////////////////////////////////////
//The Begin
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
//Or enable:
//<script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>;
//var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//The End
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////







// dish_add.html & dish_edit.html JS ////////////////////////////////////////////////////////////////////////////////////////////////////
//The Begin

// Add ingredient to dish on submit
$('#dish_ingredient_submit_btn').click(function(event){

    event.preventDefault();
    addIngredientDish();
});

function addAddedIngredientDish() {

    var values = $("input[id='dish_ingredient_added']").map(function(){return $(this).val();}).get();
    for (i in values) {
    var ingredientAdded=JSON.parse(values[i]);

    addIngredientDish(addedIngredient=true,ingredientAdded.id,ingredientAdded.quantity,ingredientAdded.name, ingredientAdded.unit);
    };
};



function addIngredientDish(addedIngredient=false,ingredientId=null,ingredientQuantity=null,ingredientName=null, ingredientUnit=null) {

    if (addedIngredient==false){
        var ingredientId = $('#dish_ingredient option:selected').val();
        var ingredientQuantity = $('#dish_ingredient_quantity').val();
        var ingredientName=$("#dish_ingredient option:selected").text().split(' | ',1)+'';
        var ingredientUnit=$("#dish_ingredient option:selected").text().split(' | ',2)[1]+'';

        }
    else{
        var ingredientId = ingredientId;
        var ingredientQuantity = ingredientQuantity;
        var ingredientName=ingredientName;
        var ingredientUnit=ingredientUnit;

        $("#dish_ingredient option[value="+ingredientId+"]").attr('disabled','disabled')

    };

    //create custom link element of ordered ingredient
    var ingredientIdName=ingredientName.split(' ').join('_');
    var $newIngred = $("<a id='"+ingredientId+"-a_id_"+ingredientIdName+"' class='list-group-item list-group-item-action d-flex justify-content-between align-items-center my-delete-link'>Delete "+ ingredientName +"<input type='hidden' form='dish_add_form'  id='dish_ingredient' name='dish_ingredient' value='"+ingredientId+'|'+ingredientQuantity+"'><span class='badge badge-primary badge-pill'>"+ingredientQuantity+" "+ingredientUnit+"</span></a>");


    // add ingredient element to list
    $("#dish_ingredient option:selected").attr('disabled','disabled')
    $('#dish_ingredient').val(null); // remove the value from the select
    $('#dish_ingredient_submit_btn').attr('disabled', true);
    $("#ingredient_list_div").prepend($newIngred);

    // delete ingredient element from list
    $newIngred.bind( "click", function() {
           event.preventDefault();
           var delIngredientId=parseInt($(this).attr("id").split('-',1));
           $("#dish_ingredient option[value=" + delIngredientId + "]").removeAttr('disabled');
           var $ing = $('#'+$(this).attr("id"));
           $ing.remove();

    });
    };

function addIngredientAjax() {
    $.ajax({
        url : "ingredient/", // the endpoint
        type : "POST", // http method
        data : { action:'add', ingredient_id : $('#dish_ingredient').val(), ingredient_quantity: $('#dish_ingredient_quantity').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {

            // create custom link element of ordered ingredient
            var ingredientIdName=json.new_added_ingredient.name.split(' ').join('_');
            var $newIngred = $( "<a id='"+json.new_added_ingredient.id+"-a_id_"+ ingredientIdName +"' class='list-group-item list-group-item-action d-flex justify-content-between align-items-center my-delete-link'>Delete "+ json.new_added_ingredient.name +"<span class='badge badge-primary badge-pill'>"+json.new_added_ingredient.quantity+" "+json.new_added_ingredient.unit+"</span></a>");

            // delete ingredient element from list
            $newIngred.bind( "click", function() {
                event.preventDefault();
                var delIngredientId=parseInt($(this).attr("id").split('-',1));
                $("#dish_ingredient option[value=" + delIngredientId + "]").removeAttr('disabled');
                var $ing = $('#'+$(this).attr("id"));
                $ing.remove();
                var url = "ingredient/";
                $.post(url, { action: 'delete', id_deleted_ingredient: delIngredientId });
            });

            // add ingredient element to list
            $("#dish_ingredient option:selected").attr('disabled','disabled')
            $('#dish_ingredient').val(null); // remove the value from the select
            $('#dish_ingredient_submit_btn').attr('disabled', true);
            $("#ingredient_list_div").prepend($newIngred);

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
//The End
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// order_add.html JS ////////////////////////////////////////////////////////////////////////////////////////////////////
//The Begin

// Add ingredient to order on submit
$('#order_ingredient_submit_btn').click(function(event){

    event.preventDefault();
    addIngredientOrder();
});

function addAddedIngredientOrder() {

    var values = $("input[id='order_ingredient_added']").map(function(){return $(this).val();}).get();
    for (i in values) {
    var ingredientAdded=JSON.parse(values[i]);

    addIngredientOrder(addedIngredient=true,ingredientAdded.id,ingredientAdded.quantity,ingredientAdded.name, ingredientAdded.unit, ingredientAdded.cost);
    };
};



function addIngredientOrder(addedIngredient=false,ingredientId=null,ingredientQuantity=null,ingredientName=null, ingredientUnit=null, ingredientCost=null) {

    if (addedIngredient==false){
        var ingredientId = $('#order_ingredient option:selected').val();
        var ingredientQuantity = $('#order_ingredient_quantity').val();
        var ingredientName=$("#order_ingredient option:selected").text().split('|',1)+'';
        var ingredientUnit=$("#order_ingredient option:selected").text().split('|',2)[1]+'';
        var ingredientCost=$("#order_ingredient_cost").val()
        }
    else{
        var ingredientId = ingredientId;
        var ingredientQuantity = ingredientQuantity;
        var ingredientName=ingredientName;
        var ingredientUnit=ingredientUnit;
        var ingredientCost=ingredientCost;


        $("#order_ingredient option[value="+ingredientId+"]").attr('disabled','disabled')
    };

    // add ingredient cost to total
    var total= parseFloat($('.order-total').val());
    total+=parseFloat(ingredientCost);
    $('.order-total').val(total.toFixed(2));

    //create custom link element of ordered ingredient
    var ingredientIdName=ingredientName.split(' ').join('_');
    var $newOrderIngred = $("<a id='"+ingredientId+"-a_id_"+ingredientIdName+"' class='list-group-item list-group-item-action d-flex justify-content-between align-items-center my-delete-link'>Delete "+ ingredientName +"<input type='hidden' form='order_add_form'  id='order_ingredient' name='order_ingredient' value='"+ingredientId+'|'+ingredientQuantity+'|'+ingredientCost+"'><span class='badge badge-primary badge-pill'>"+ingredientQuantity+" "+ingredientUnit+"</span>  <span class='badge badge-primary badge-pill'>"+ingredientCost+" UAH</span></a>");


    // add ingredient element to list
    $("#order_ingredient option:selected").attr('disabled','disabled')
    $('#order_ingredient').val(null); // remove the value from the select
    $('#order_ingredient_quantity').val(null); // remove the value from the quantity
    $('#order_ingredient_cost').val(null); // remove the value from the cost
    $('#order_ingredient_submit_btn').attr('disabled', true);
    $("#order_ingredient_list_div").prepend($newOrderIngred);

    // delete ingredient element from list
    $newOrderIngred.bind( "click", function() {
           event.preventDefault();

           // remove ingredient cost from total
           var total= parseFloat($('.order-total').val());
           var ingredientData=$(this).children("input").val()
           var ingredientCost=ingredientData.split('|',3)[2]+'';
           total-=parseFloat(ingredientCost);
           $('.order-total').val(total.toFixed(2));

           var delIngredientId=parseInt($(this).attr("id").split('-',1));
           $("#order_ingredient option[value=" + delIngredientId + "]").removeAttr('disabled');
           var $ing = $('#'+$(this).attr("id"));
           $ing.remove();

    });
    };


//The End
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




$(document).ready(function () {



// dish_add.html & dish_edit.html JS //////////////////////////////////////////////
//The Begin

    $('#dish_ingredient_submit_btn').attr('disabled', true);

    $('#dish_ingredient,#dish_ingredient_quantity').on('change', function () {
        var selectValue = $("#dish_ingredient").val();
        var inputValue = $('#dish_ingredient_quantity').val();
        if (selectValue != null && inputValue != '') {
            $('#dish_ingredient_submit_btn').attr('disabled', false);
        } else {
            $('#dish_ingredient_submit_btn').attr('disabled', true);
        }
    });

    $('.custom-file-input').on('change',function(){
                var fileName = $(this).val();
                $(this).next('.custom-file-label').html(fileName);
    });

    addAddedIngredientDish();

//The End
///////////////////////////////////////////////////////////////////////////////////

// order_add.html JS //////////////////////////////////////////////////////////////
//The Begin

    if (typeof orderCounter === 'undefined'){
        var orderCounter=0;
        $('#order_counter').text(orderCounter);
    };


    $('#order_ingredient_submit_btn').attr('disabled', true);

    $('#order_ingredient,#order_ingredient_quantity').on('change', function () {
        var selectValue = $("#order_ingredient").val();
        var inputValue = $('#order_ingredient_quantity').val();
        if (selectValue != null && inputValue != '') {
            $('#order_ingredient_submit_btn').attr('disabled', false);
        } else {
            $('#order_ingredient_submit_btn').attr('disabled', true);
        }
    });

    $('#order_ingredient_quantity,#order_ingredient').on('click',function(){

                if($("#order_ingredient option:selected").val()){
                   var cost=$("#order_ingredient option:selected").text().split('|',3)[2]+'';
                   cost=parseFloat(cost);
                   var quantity=$('#order_ingredient_quantity').val();
                   var total=quantity*cost/10;
                   $("#order_ingredient_cost").val(total.toFixed(2));
                };
    });

    addAddedIngredientOrder();

//The End
///////////////////////////////////////////////////////////////////////////////////
});


