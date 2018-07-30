jQuery(function() {
	$('#marks_').val('[]');
	$(document).keypress(function() {
		var marks = $('#marks_').val();
		console.log(marks);
		marks = JSON.parse(marks);
		var now = new Date(Date.now()).toISOString();
		marks.push(replaceAll(replaceAll(replaceAll(now, ":", "-"), "T", " "), "Z", ""));
		$('#marks_').val(JSON.stringify(marks));
	});

	function replaceAll(str, find, replace) {
	    return str.replace(new RegExp(find, 'g'), replace);
	}
});
