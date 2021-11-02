window.addEventListener("load", function() {
    (function($) {
        $('.copy-btn').on('click', function(e){
            // To-Do: Find a better way to select the participants emails
            // console.log('emails:',$(this).parent().prev().text());
            e.preventDefault();
            var $temp = $("<input>");
            $("body").append($temp);
            $temp.val($(this).parent().prev().text()).select();
            var check = document.execCommand("copy");
            $temp.remove();
        });
    })(django.jQuery);
});
