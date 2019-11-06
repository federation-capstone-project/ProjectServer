
(function ($) {
    "use strict";

    var input = $('.validate-input .input100');

    $('.validate-form').on('submit', function () {
        var check = true;

        for (var i = 0; i < input.length; i++) {
            
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });
    

    $("#id_password1").focusout(function () {
     
        $('#password-strength-status').removeClass();
        $('#password-strength-status').html('');
    });

    

    $("#id_password1").keyup(function () {

        var number = /([0-9])/;
        var alphabets = /([a-zA-Z])/;
        var special_characters = /([~,!,@,#,$,%,^,&,*,-,_,+,=,?,>,<])/;
        if ($('#id_password1').val().length < 6) {
            $('#password-strength-status').removeClass();
            $('#password-strength-status').addClass('weak-password');
            $('#password-strength-status').html("*Weak (should be atleast 8 characters.)");
        } else {
            if ($('#id_password1').val().match(number) && $('#id_password1').val().match(alphabets) && $('#id_password1').val().match(special_characters)) {
                $('#password-strength-status').removeClass();
                $('#password-strength-status').addClass('strong-password');
                $('#password-strength-status').html("*Strong");
            } else {
                $('#password-strength-status').removeClass();
                $('#password-strength-status').addClass('medium-password');
                $('#password-strength-status').html("*Medium (should include alphabets, numbers and special characters.)");
            }
        }
    });
    

    function checkPassword(str) {
        //var re = /^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])[\w!@#$%^&*]{8,}$/;
        var re = /^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*])[\w!@#$%^&*]{8,}$/;
        return re.test(str);
    }



    function validate(input) {
        if ($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if ($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {

            if ($(input).val().trim() == '') {
                return false;
            }

            if ($(input).val().trim() != '' && ($(input).attr('id') == "id_password1") && $("#id_password1").val() != null)
            {
                var checkpassword = checkPassword($("#id_password1").val());
                if (!checkpassword)
                {
                    return false;
                }
            }


            if ($(input).val().trim() != '' && ($(input).attr('id') == "id_password2")
                && $("#id_password1").val() != null && $("#id_password2").val() != null
                && $("#id_password1").val() != $("#id_password2").val())
            {
                $('#password-strength-status').removeClass();
                $('#password-strength-status').addClass('password-not-matched');
                $('#password-strength-status').html("password not match please try again.");
                return false;
            }

        }
    }

    function showValidate(input) {

        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }


    var showPass = 0;
    $('.btn-show-pass').on('click', function () {
        if (showPass == 0) {
            $(this).next('input').attr('type', 'text');
            $(this).find('i').removeClass('fa-eye');
            $(this).find('i').addClass('fa-eye-slash');
            showPass = 1;
        }
        else {
            $(this).next('input').attr('type', 'password');
            $(this).find('i').removeClass('fa-eye-slash');
            $(this).find('i').addClass('fa-eye');
            showPass = 0;
        }

    });


})(jQuery);