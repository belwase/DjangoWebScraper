
$(document).ready(function() {

	var auto_refresh = setInterval(
		function(){

				                    //Get all ids
	                    var ids = [];
	                    $("tr[id^='crawler_status_']").each(function() {
	                     ids.push(this.id.match(/\d+/)[0])
	                    });

	             $.ajax({
                    url : '/auto_refresh/',
                    async:true,
                    data:{'id':ids.toString()},
                    type:'GET',
                    success : function(data) {


	                    jQuery.each(data, function(index, item) {
	                    		//console.log('Ajax id :'+typeof(item.id) + ' , table id :'+typeof(ids) + typeof(ids[0]) + ' , result ' + $.inArray( parseInt(item.id) ,ids ))
	                            if( $.inArray( item.id.toString() , ids ) >=0 ) {
	                                    $("tr#crawler_status_"+item.id).replaceWith(item.row);
	                                    
	                             }else{ 
	                                   $('table[id=crawler_status_table]').append(item.row)
	                            }
	                    });
                    },
                    error : function() {
                        console.log('error');
                    }
            });

}, 10000); // refresh every 10000 milliseconds (10 sec)


	show_default_tab();

	$('a[href$=primary]').click(function(e){
//alert($(e.target));
		var site = $(e.target).text();
		//alert(site);

		switch(site){

			case 'Tripadvisor':
				$('div[id$=primary]').hide();
				$('div[id=tab2primary]').show();
				break;
			case 'Facebook':
				$('div[id$=primary]').hide();
				$('div[id=tab3primary]').show();
				break;
			case 'Yelp':
				$('div[id$=primary]').hide();
				$('div[id=tab4primary]').show();
				break;
			default:
				show_default_tab();
		}

	});
/*	
	$('div[id$=_box]').hide();
	$('div[id=main_box]').hide();

	$('.site_dropdown').click(function(e){
		var site = $(e.target).text();
		//alert(site);

		switch(site){

			case 'Tripadvisor':
				$('div[id$=_box]').hide();
				$('div[id = trip_box]').show();
				break;
			case 'Facebook':
				$('div[id$=_box]').hide();
				$('div[id = fb_box]').show();
				break;
			default:
		}
	});
*/

	$('.cancel_box').click(function(e){
		$(this).closest('div[id$=_box]').hide();

	});

	$('.option_dropdown').click(function(e){
		var selected_option = $(e.target).text();
		$(this).closest('ul').prev().text(selected_option);
		var parent_class = $(this).parent()[0].className;
		$('input[name='+parent_class+']').val($(e.target).attr('value'));
		
		//console.log($(e.target).attr('value'));
		//var nearby_input = $(this).closest('input');
		//console.log(nearby_input);
		//nearby_input.val($(e.target).attr('value'));
		//alert($(e.target).text());
		//alert($(this).siblings());
		//$(this).closest('button').text($(e.target).text());
	});
/*
	$( "form" ).on( "submit", function( event ) {
	  event.preventDefault();
	  console.log( $( this ).serialize() );
	});

*/

	$('.form_button').click(function(e){
			var form = $(this).closest('form');
		    var data = form.serialize();
	        $.ajax({
	                async:true,
	                type:"POST",
	                data:data,
	                url:'/process_form/',
	                success: function(data){
	                        //$.LoadingOverlay("hide");
	                        
	                        //var json = $.parseJSON(data);
	                        var json = jQuery.parseJSON(JSON.stringify(data));
	                        if ( json.status == "1" ){
	                                alert('Done : ' + json.msg);
	                        }else{
	                        	alert('Error while crawling : '+json.msg)
	                        }
	                    show_default_tab();
	                }

	        });
	});

});

function show_popup(source){

	if(source = 'facebook_token'){
		alert('Login to your facebook account. \n Goto https://developers.facebook.com/tools/explorer/ \n Copy Access token from box');
	}


}

function show_default_tab()
{
	$('div[id$=primary]').hide();
	$('div[id=tab1primary]').show();

}
