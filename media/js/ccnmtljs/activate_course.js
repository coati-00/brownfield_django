//function edit_students(){

//	var data = [];
//	
//    //jQuery('#student_team_tables tr').each(
//	jQuery('.student-row').each(
//        function(){
//            var student = {'pk': jQuery(this).find("td input[name='std-id']").val(),
//				           'first_name': jQuery(this).find("td input[name='first_name']").val(), 
//				           'last_name': jQuery(this).find("td input[name='last_name']").val(), 
//				           'email': jQuery(this).find("td input[name='email']").val(),
//				           'team_id': jQuery(this).find("td option:selected").val(),
//				           'team_name': jQuery(this).find("td option:selected").text()
//                           }
//      data.push({ 'student' : student });
//            
//    })
//
//    return data;
//}

function get_students(){

	var data = [];
	
    //jQuery('#student_team_tables tr').each(
	jQuery('.student-row').each(
        function(){
            var student = {'pk': jQuery(this).find("td input[name='std-id']").val(),
				           'first_name': jQuery(this).find("td input[name='first_name']").val(), 
				           'last_name': jQuery(this).find("td input[name='last_name']").val(), 
				           'email': jQuery(this).find("td input[name='email']").val(),
				           'team_id': jQuery(this).find("td option:selected").val(),
				           'team_name': jQuery(this).find("td option:selected").text()
                           }
      data.push({ 'student' : student });
            
    })

    return data;
}

jQuery(function() {
	
	var crs_id = jQuery("input[name='crs-id']").val();

	jQuery('#activation-btn').on('click', function(e)
    {   
		var student_list = get_students();
        var student_list_2 =JSON.stringify(student_list);

        jQuery(function()
    	{
    	   	jQuery.ajax(
    	    {
    	        url: "/activate_course/" + crs_id,
    	    	type: "POST",
    	    	dataType: 'json',
    	    	data: {'student_list' : student_list_2},
    	    	success: function (data) 
    	    	{
    	    		//alert('Success');
    	    		//jQuery("#activation-btn").click();
        	    },
	    	           
        	    error: function(data) 
	    	    {
        	    	alert('Something went wrong, please try again');
	    	    }
        	}); // end ajax POST
    	
    	}); // end inner on click function
    	
        e.preventDefault(); //we don't want the form submitting

    });// end on click function
});

jQuery(function() {
	
	var crs_id = jQuery("input[name='crs-id']").val();

	jQuery('#edit-team-members').on('click', function(e)
    {   
		jQuery(".course-teams").load("/edit_teams/" + crs_id + "/");
		jQuery('#edit-team-members').hide();
		jQuery('#show-teams').show();

    });// may need prevent default....
});

jQuery(function() {
	
	var crs_id = jQuery("input[name='crs-id']").val();

	jQuery('#show-teams').on('click', function(e)
    {   console.log("inside show teams on click");
		jQuery(".course-activation").load("/show_teams/" + crs_id + "/");
		jQuery('#show-teams').hide();
		jQuery('#edit-team-members').show();
    });// may need prevent default....
});