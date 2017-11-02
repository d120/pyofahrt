$(document).ready(function () {
 
    $('[data-toggle="tooltip"]').tooltip();
 
    $("#unassigned").find(".workshop").each(function (index) {
        // Einsortieren aller Workshops in die Workshop-Tabelle
 
        element = $(this);
        if (element.attr("data-init-room") === 0 && element.attr("data-init-slot") === 0) {
            // Noch nicht zugeteilt
            return;
        } else {
            $("td[data-room='" + element.attr("data-init-room") + "'][data-slot='" + element.attr("data-init-slot") + "']").append(element);
        }
    });
 
    $(".sortablearea").sortable({
        connectWith: ".sortablearea",
        receive: function (event, ui) {
            var room = ui.item.parent().attr("data-room");
            var slot = ui.item.parent().attr("data-slot");
            var workshop = ui.item.attr("data-workshop");
            var obj = {room: room, slot: slot, workshop: workshop};
 
            $.getJSON(ajaxurl, obj, function (data) {
                // TODO
                if (data.conflicts === "[]") {
                    console.log("no conflicts");
                } else {
                    console.log("conflicts:");
                    console.log(data.conflicts);
                }
            });
        }
    }).disableSelection();
 
    var workshop = $('.workshop');
 
    workshop.mousedown(function () {
        $(this).tooltip('disable');
        $(this).tooltip('hide');
    });
 
    workshop.mouseup(function () {
        $(this).tooltip('enable');
    });
});
