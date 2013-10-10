$(document).ready(function() {
    $(".update").each(function(index, element) {
	$.get('update/'+$(element).attr("source"), function(data) {
	    $(element).html(data);
	});
    });
})