/* JS doc, requires jQuery */


// Need to get the CSRF cookie for AJAX posts
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


$(document).ready(function() {

  $("#searchTerms").focus();
  
  
  // Add the CSRF cookie before doing AJAX posts
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    });



  $("#btnSubmit").click(function() {
    var searchDic = {"search_terms": $("#searchTerms").val(),
        "start_val": "1"     
    };
       // "num_requests": $("#numResults").val()};
    //console.log(JSON.stringify(searchDic));
    
    var numRequests = parseInt($("#numResults").val()) / 10;
    console.log("numRequests: "+ numRequests);

    for (i = 0; i < numRequests; i++) {

        searchDic["start_val"] = String(1 + (i * 10));
        $.ajax({
          "type": "POST",    
          "url": "gsearch_requester",
          "data": JSON.stringify(searchDic),
          "beforeSend": function(xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
          },
          "success": function(result) {
              console.log(result);
          },
          "dataType": "json",
        });
        
        var msg = (i + 1) * 10 + " results returned<br>";
        $("#resultsArea").append(msg);
        
        
    }

    
  });

});