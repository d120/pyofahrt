$(document).ready(function () {

    $('[data-toggle="tooltip"]').tooltip();

    // iterate over all workshops
    $("#unassigned").find(".workshop").each(function (index) {

        element = $(this);
        if (element.attr("data-init-room") === 0 && element.attr("data-init-slot") === 0) {
            // if workshop is not asserted:
            return;
        } else {
            // else (if workshop has assertion)
            $("td[data-room='" + element.attr("data-init-room") + "'][data-slot='" + element.attr("data-init-slot") + "']").append(element);
        }
    });

    $(".sortablearea").sortable({
        connectWith: ".sortablearea",
        receive: function (event, ui) {
            // collect information of moved workshop:
            var room = ui.item.parent().attr("data-room");
            var slot = ui.item.parent().attr("data-slot");
            var workshop = ui.item.attr("data-workshop");
            var obj = {room: room, slot: slot, workshop: workshop};

            // save it
            $.getJSON(ajaxurl, obj);

            // check for conflicts
            highlightConflicts();
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

    function highlightConflicts() {
        // check for conflicts and change displaying color if necessary
        $.getJSON(ajaxurl2, function (data) {
            // iterate over all workshop elements in the planer
            $('[data-workshop]').each(function () {
                let workshopID = parseInt($(this).attr("data-workshop"));

                // change the appearance accordingly
                if (data.conflicts.includes(workshopID)) {
                    $(this).addClass("conflict")
                } else {
                    $(this).removeClass("conflict")
                }
            });
        });
    }

    window.onload = function () {
        highlightConflicts();
    };
});
