$( document ).ready(function() {
                
    $("#message").fadeOut();   
    $("#collect").fadeOut();

    $("#my_message").click(function(){
        $("#info").fadeOut();
        $("#collect").fadeOut();
        $("#message").fadeIn();
        });
    $("#my_collect").click(function(){
        $("#info").fadeOut();
        $("#message").fadeOut();
        $("#collect").fadeIn();
        });

    $("#my_info").click(function(){
        $(".pages").fadeOut();
        $("#info").fadeIn();
        });

});