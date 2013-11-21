$(document).ready(function() {
    h3 = document.getElementById('fetiontext').scrollHeight;
    h1 = document.getElementById('oldfetion2').scrollHeight;
    h2 = document.getElementById('oldfetion1').scrollHeight;
    max = h1 > h2 ? h1 : h2;
    max = h3 > max? h3 : max;
    $('#fetiontext').height(max);
    $('#fetiontext').keyup(function(e) {
	$(this).height(max);
	$(this).height(this.scrollHeight);
	$('#submit').zclip('remove')
	$('#submit').zclip({
	    path:'/static/js/zclip.swf',
	    copy: submit,
	    afterCopy: function() {
	    }
	});
    });
    $('#submit').zclip({
	path:'/static/js/zclip.swf',
	copy: submit,
	afterCopy: function() {
	}
    });
    //$('#submit').tooltip();
})

function submit() {
    text = document.getElementById('fetiontext');
    return text.value.trim() + "\n"
}