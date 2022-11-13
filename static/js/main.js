$(document).ready(function () {
	$("#search-query").focus();
});

$("#advanced-search-button").click(function () {
	$(".advanced-search-panel").slideToggle("fast");
	$(this).toggleClass("active");
});

$(document).ready(function ($) {
	$("#tabs").tab();
});

function update_result(data) {
	var result_list = $("#result-list-group");
	result_list.empty();
	console.log(data);

	var tab_html = '<ul class="nav nav-tabs" role="tablist">';
	tab_html +=
		'<li role="presentation"><a href="#all" aria-controls="all" role="tab" data-toggle="tab">All</a></li>';
	var tab_content_html = "";
	var all_html = '<div role="tabpanel" class="tab-pane tab-body" id="all">';
	all_html += '<div class="list-group">';

	var count = 0;


	for (var conf in data[0]) {
		var flag = false;
		var conf_html =
			'<div role="tabpanel" class="tab-pane tab-body" id="' + conf + '">';
		conf_html += '<div class="list-group">';
		for (
			var year_i = Object.keys(data[0][conf]).length - 1; year_i >= 0; year_i--
		) {
			// console.log(data[0][conf]);
			// console.log(year_i);
			// console.log(Object.keys(data[0][conf]));
			// check has key year
			if (Object.keys(data[0][conf])[year_i] == undefined) {
				continue;
			}

			var year = Object.keys(data[0][conf])[year_i];
			for (var i in data[0][conf][year]) {
				var title = data[0][conf][year][i]["title"];
				var url = data[0][conf][year][i]["url"];
				var authors = data[0][conf][year][i]["authors"];
				var abstract = data[0][conf][year][i]["abstract"];
				var code = data[0][conf][year][i]["code"];
				var citation = data[0][conf][year][i]["citation"];
				if (abstract == null || abstract == "") {
					abstract = "No abstract available";
				}
				if (code == null || code == "" || code == "#") {
					code = "https://paperswithcode.com/search?q=" + title;
				}

				// replace < and > with &lt; and &gt; in abstract
				abstract = abstract.replace(/</g, "&lt;");
				abstract = abstract.replace(/>/g, "&gt;");

				// console.log(title);
				// console.log(url);
				// console.log(authors);
				// console.log(abstract);
				// console.log("\n");

				var author_html = "";
				for (var j in authors) {

					var conf_idx = location.href.indexOf('&confs');
					var author_query = '/r?query=&year=&sp_year=&sp_author=' + authors[j] + location.href.substring(conf_idx);


					author_html += '<li class="author-item">' +
						'<a href="' + author_query + '" >' +
						authors[j] + "</a>" + "</li>";
				}
				author_html = '<ul class="authors">' + author_html + "</ul>";

				var abstract_id = `abs-${i}-${conf}${year}`;
				var abstract_button = `
        <a class="abstract" href="#${abstract_id}" data-toggle="collapse" data-target="#${abstract_id}" aria-expanded="false" aria-controls="${abstract_id}">abstract</a>`;

				var abstract_item = `
        <div id="${abstract_id}" class="collapse">
        <div class="abstract-item">${abstract}</div>
        </div>`;

				flag = true;
				var item_html = "";
				item_html += '<div class="panel panel-default list-group-item">';
				item_html += '<div class="panel-body">';
				item_html += '<div class="media" style="display:flex;">';


				item_html += '<div class="media-body">';
				item_html += '<a href="' + url + '" target="_blank">';
				item_html += '<h4 class="media-heading">' + title + "</h4>";
				item_html += "</a>";
				item_html += abstract_button;
				item_html += author_html;
				item_html += abstract_item;
				item_html +=
					'<p class="media-item"><span class="label label-success">' +
					conf +
					year +
					"</span>" +
					'<a href="' + code + '" style="text-decoration:none; margin-left:5px;"><span class="label label-info">Code</span></a>' + 
					'<a style="text-decoration:none; margin-left:5px;" class="label label-warning" title="BibTeX" data-container="body" data-toggle="bibtex" data-placement="right" data-content="Under Construction">BibTeX</a>' +
					"</p>";
				item_html += "</div>";

				item_html += '<div class="delete-btn" style="margin-left: auto; margin-right: 0; display: flex; justify-content: flex-end;">'
				item_html += '<a href="javascript:void(0)"><img src="static/delete.svg" width="50%" height="100%"></a>'
				item_html += "</div>";

				item_html += "</div>";
				item_html += "</div>";
				item_html += "</div>";

				all_html += item_html.replaceAll(
					`${abstract_id}`,
					`${abstract_id}-all`
				);
				conf_html += item_html;
				count++;
			}
		}
		conf_html += "</div>";
		conf_html += "</div>";
		if (flag) {
			tab_html +=
				'<li role="presentation"><a href="#' +
				conf +
				'" aria-controls="' +
				conf +
				'" role="tab" data-toggle="tab">' +
				conf +
				"</a></li>";
			tab_content_html += conf_html;
		}
	}

	all_html += "</div>";
	all_html += "</div>";
	tab_content_html =
		'<div class="tab-content">' + all_html + tab_content_html + "</div>";

	tab_html += "</ul>";
	// console.log(tab_html);
	// console.log(tab_content_html);

	var prompt_html = "";
	if (count == 0) {
		prompt_html =
			'<div class="alert alert-warning text-center" role="alert">No result found.</div>';
	} else {
		prompt_html =
			'<div class="alert alert-success text-center" role="alert">' +
			count +
			" result(s) found.</div>";
	}

	$("#result-list-group").html(prompt_html + tab_html + tab_content_html);
	$("#result-list-group .tab-body").first().addClass("active");
	$("#result-list-group .nav-tabs li").first().addClass("active");
    $(function () { 
      $("[data-toggle='bibtex']").popover();
    });
	$("li[role='presentation']").on("click", function() {
		// clear the delete_items
		delete_items = [];
	});
	//click the delete-item tag to remove div
	$(".delete-btn a").on("click", function() {
		if (typeof delete_items != "undefined") {
			//get media-heading
			var title = $(this).parent().parent().find(".media-heading").text();
			delete_items.push(title);
		}
		$(this).parents(".list-group-item").remove();
	});
}

function JSONToCSVConvertor(data, tab) {
	var csv = "";
	let row = "";
	let _item = ['title', 'url', 'authors', 'abstract', 'code', 'citation'];
	for (var index in _item) {
		row += _item[index] + ',';
	}
	row += 'conf,year';
	csv += row + '\r\n';
	for (var conf in data[0]) {
		if (tab != "all" && conf != tab) {
			continue;
		}
		for (var year in data[0][conf]) {
			for (var i in data[0][conf][year]) {
				let item = data[0][conf][year][i];
				if (item == null) {
					continue;
				}
				if (delete_items.includes(item["title"])) {
					continue;
				}
				let row = "";
				for (var index in item) {
					row += '"' + item[index] + '",';
				}
				row += conf + ',' + year;
				csv += row + '\r\n';
			}
		}
	}
	return csv;
}

function JSONToText(data, tab) {
	var txt = "";
	for (var conf in data[0]) {
		if (tab != "all" && conf != tab) {
			continue;
		}
		for (var year in data[0][conf]) {
			for (var i in data[0][conf][year]) {
				let item = data[0][conf][year][i];
				if (item == null) {
					continue;
				}
				if (delete_items.includes(item["title"])) {
					continue;
				}
				let row = "[" + conf + year + "]\t" + item["title"];
				txt += row + '\r\n';
			}
		}
	}
	return txt;
}

function export_result_to_csv(data) {
	let tab = $(".active[role='presentation'] a").attr('aria-controls')
	let csv = JSONToCSVConvertor(data, tab);
	let dataUri =
		"data:text/csv;charset=utf-8," + encodeURIComponent(csv);
	let exportFileDefaultName = "result.csv";
	let linkElement = document.createElement("a");
	linkElement.setAttribute("href", dataUri);
	linkElement.setAttribute("download", exportFileDefaultName);
	linkElement.click();
}

function export_result_txt(data) {
	let tab = $(".active[role='presentation'] a").attr('aria-controls')
	let txt = JSONToText(data, tab);
	let dataUri =
		"data:text/plain;charset=utf-8," + encodeURIComponent(txt);
	let exportFileDefaultName = "result.txt";
	let linkElement = document.createElement("a");
	linkElement.setAttribute("href", dataUri);
	linkElement.setAttribute("download", exportFileDefaultName);
	linkElement.click();
}

function export_result(data) {
	let dataStr = JSON.stringify(data);
	let dataUri =
		"data:application/json;charset=utf-8," + encodeURIComponent(dataStr);
	let exportFileDefaultName = "result.json";
	let linkElement = document.createElement("a");
	linkElement.setAttribute("href", dataUri);
	linkElement.setAttribute("download", exportFileDefaultName);
	linkElement.click();
}

$("#export-button").click(function () {
	if (typeof data !== "undefined") {
		export_result_to_csv(data);
		export_result_txt(data);
		// export_result(data);
	}
});

$("#research-button").click(function () {
	// check whether have data variable
	if (typeof data !== "undefined") {
		// console.log(data);
		// get text from input
		var query = $("#query").val();
		query = query.toLowerCase();
		query = query.replace(/\s+/g, " ");
		query = query.replace("-", " ");
		query = query.trim();
		// console.log(query);

		var sp_author = $("#sp_author").val();
		sp_author = sp_author.toLowerCase();
		sp_author = sp_author.replace(/\s+/g, " ");
		sp_author = sp_author.replace("-", " ");
		sp_author = sp_author.trim();

		var sp_year = $("#sp_year").val();
		sp_year = sp_year.trim();
		if (sp_year != "") {
			sp_year = parseInt(sp_year);
		}

		data_ = {};

		// search for query
		for (var conf in data[0]) {
			data_[conf] = {};
			for (var year in data[0][conf]) {
				data_[conf][year] = [];
				for (var i in data[0][conf][year]) {
					console.log(data[0][conf][year][i]);

					if (sp_year != "" && sp_year != year) {
						continue;
					}

					var title = data[0][conf][year][i]["title"].toLowerCase();
					title = title.replace(/\s+/g, " ");
					title = title.replace("-", " ");
					title = title.trim();

					var author = data[0][conf][year][i]["authors"].join(" ").toLowerCase();
					author = author.replace(/\s+/g, " ");
					author = author.replace("-", " ");
					author = author.trim();

					if (title.indexOf(query) != -1) {
						if (sp_author == "") {
							data_[conf][year].push(data[0][conf][year][i]);
						} else {
							if (author.indexOf(sp_author) != -1) {
								data_[conf][year].push(data[0][conf][year][i]);
							}
						}
					}
				}
			}
		}
		data = [];
		data.push(data_);
		update_result(data);
	}
});

$("#conf-select-all").click(function () {
	$('input[name="confs"]').prop("checked", true);
});

$("#conf-select-none").click(function () {
	$('input[name="confs"]').prop("checked", false);
});

$("#conf-invert").click(function () {
	$('input[name="confs"]').each(function () {
		$(this).prop("checked", !$(this).prop("checked"));
	});
});