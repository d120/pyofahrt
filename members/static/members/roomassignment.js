$( function() {
  $( ".sortablearea" ).sortable({
      connectWith: ".sortablearea",
      receive: function( event, ui ) {

        var toFullLabel = " <span class=\"label label-danger\">zu voll!</span>";

        newroomid = ui.item.parent().parent().attr("id");
        oldroomid = ui.sender.parent().attr("id");

        //Zähler neu setzen
        newelements = $("#" + newroomid + " > .sortablearea").children().length;
        oldelements = $("#" + oldroomid + " > .sortablearea").children().length;
        $("#" + newroomid + " .counter").text(newelements);
        $("#" + oldroomid + " .counter").text(oldelements);

        //Überfüllung prüfen
        newmax = parseInt($("#" + newroomid + " .max").text());
        oldmax = parseInt($("#" + oldroomid + " .max").text());

        if(newelements > newmax && !$("#" + newroomid).hasClass("fullroom")){
          $("#" + newroomid).addClass("fullroom");
          $("#" + newroomid + " .roomtitle").append(toFullLabel);
        }
        else if(newelements <= newmax && $("#" + newroomid).hasClass("fullroom"))
        {
          $("#" + newroomid).removeClass("fullroom");
          $("#" + newroomid + " .label").remove();
        }

        if(oldelements > oldmax && !$("#" + oldroomid).hasClass("fullroom")){
          $("#" + oldroomid).addClass("fullroom");
          $("#" + oldroomid + " .roomtitle").append(toFullLabel);
        }
        else if(oldelements <= oldmax && $("#" + oldroomid).hasClass("fullroom"))
        {
          $("#" + oldroomid).removeClass("fullroom");
          $("#" + oldroomid + " .label").remove();
        }

      }
    }).disableSelection();
} );
