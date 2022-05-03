$(document).ready(function() {
	$('#search-query').focus();
});

$('#advanced-search-button').click(function() {
	$('.advanced-search-panel').slideToggle('fast');
	$(this).toggleClass('active');
});

$(document).ready(function ($) {
    $('#tabs').tab();
});

$('#research-button').click(function() {
	// check whether have data variable
	if (typeof data !== 'undefined') {
		// console.log(data);
		// get text from input
		var query = $('#query').val();
		query = query.toLowerCase();
		query = query.replace(/\s+/g, ' ');
		query = query.replace('-', ' ');
		query = query.trim();
		// console.log(query);

		data_ = {};

		// search for query
		for(var conf in data[0]) {
			data_[conf] = {};
			for(var year in data[0][conf]) {
				data_[conf][year] = [];
				for(var i in data[0][conf][year]) {
					var name = data[0][conf][year][i].toLowerCase();
					name = name.replaceAll(/\s+/g, ' ');
					name = name.replaceAll('-', ' ');
					name = name.trim();
					// console.log(name);
					if (name.indexOf(query) != -1) {
						data_[conf][year].push(data[0][conf][year][i]);
					}
				}
			}
		}
		data = [];
		data.push(data_);
		// console.log(data);
		update_result(data);
	}
});