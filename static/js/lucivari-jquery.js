$(document).ready(function() {
    $("#about-btn").click(function(event) {
        alert("You clicked the button using JQuery!");
    });
    
    $("p").hover( function() {
	    $(this).css('color', 'red');
		}, 
		function() {
		    $(this).css('color', 'blue');
	});

	$("#about-btn").click( function(event) {
	    msgstr = $("#msg").html()
	    msgstr = msgstr + "ooo"
	    $("#msg").html(msgstr)
	});

	$('.lucivari-add').click(function(){
    var catid = $(this).attr("data-catid");
    var url = $(this).attr("data-url");
    var title = $(this).attr("data-title");
    var me = $(this)
    $.get('/lucivari/add/', 
        {category_id: catid, url: url, title: title}, function(data){
            $('#pages').html(data);
            me.hide();
        });
    });

    
});