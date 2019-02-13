//Set CSRF Tokken into AJAX Request ////////////////////////////////////////////////////////////////////////////////////

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
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



// dish_add.html JS ////////////////////////////////////////////////////////////////////////////////////////////////////

// Add ingredient on submit
$('#dish_ingredient_add_form').on('submit', function(event){
    event.preventDefault();
    addIngredient();
});



// AJAX for add ingredient
function addIngredient() {
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


$(document).ready(function () {

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

});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////