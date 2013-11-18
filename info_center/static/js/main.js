$(document).ready(function() {
    $("#"+active_navbar).addClass("active");
    $(".update").each(function(index, element) {
	$.get('update/'+$(element).attr("source"), function(data) {
	    $(element).html(data);
	});
    });
})