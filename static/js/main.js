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
      var year_i = Object.keys(data[0][conf]).length - 1;
      year_i >= 0;
      year_i--
    ) {
      // console.log(data[0][conf]);
      // console.log(year_i);
      // console.log(Object.keys(data[0][conf]));
      var year = Object.keys(data[0][conf])[year_i];
      for (var i in data[0][conf][year]) {
        var title = data[0][conf][year][i]["title"];
        var url = data[0][conf][year][i]["url"];
        flag = true;
        var item_html = "";
        item_html += '<div class="panel panel-default list-group-item">';
        item_html += '<div class="panel-body">';
        item_html += '<div class="media">';
        item_html += '<div class="media-body">';
        item_html += '<a href="' + url + '" target="_blank">';
        item_html += '<h4 class="media-heading">' + title + "</h4>";
        item_html += "</a>";
        item_html += '<p class="media-item">' + conf + year + "</p>";
        item_html += "</div>";
        item_html += "</div>";
        item_html += "</div>";
        item_html += "</div>";

        all_html += item_html;
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
    export_result(data);
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

    data_ = {};

    // search for query
    for (var conf in data[0]) {
      data_[conf] = {};
      for (var year in data[0][conf]) {
        data_[conf][year] = [];
        for (var i in data[0][conf][year]) {
          console.log(data[0][conf][year][i]);
          var title = data[0][conf][year][i]["title"].toLowerCase();
          title = title.replace(/\s+/g, " ");
          title = title.replace("-", " ");
          title = title.trim();
          if (title.indexOf(query) != -1) {
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
