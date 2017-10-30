$(document).ready(function () {

    $("#unassigned .workshop").each(function (index) {
        //Einsortieren

        element = $(this);
        if (element.attr("data-init-room") == 0 & element.attr("data-init-slot") == 0) {
            //Noch nicht zugeteilt
            return;
        }
        else {
            $("td[data-room='" + element.attr("data-init-room") + "'][data-slot='" + element.attr("data-init-slot") + "']").append(element);
        }
    });

    $(".sortablearea").sortable({
        connectWith: ".sortablearea",
        receive: function (event, ui) {
            var room = ui.item.parent().attr("data-room");
            var slot = ui.item.parent().attr("data-slot");
            var workshop = ui.item.attr("data-workshop");

            obj = {room: room, slot: slot, workshop: workshop}
            $.getJSON(ajaxurl, obj);
        }
    }).disableSelection();
});