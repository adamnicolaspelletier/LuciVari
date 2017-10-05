$(document).ready(function() {
    $('#likes').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/lucivari/like_category/', {category_id: catid}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
    	});
	});
	
	$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/lucivari/suggest/', {suggestion: query}, function(data){
        $('#cats').html(data);
    	});
	});
});


