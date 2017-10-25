$(document).ready(function (e) {
    var $classy = '.panel.autocollapse';
    var $clickable = $("div.clickable");

    var $found = $($classy);
    $found.find('.panel-body').hide();
    $found.removeClass($classy);
    $clickable.unbind("click");

    $clickable.click(function (event) {
        var $this = $(this); //Heading
        var $panel = $this.parent('.panel');
        var $panel_body = $panel.children('.panel-body');
        var $display = $panel_body.css('display');

        if ($display === 'block') {
            $panel_body.slideUp();
        } else if ($display === 'none') {
            $panel_body.slideDown();
        }
    });
});