function get_students(){
	var data = [];
    jQuery('#student_team_tables tr').each(function(){
        var student = {'pk': jQuery(this).find("td input[name='std-id']").val(),
				       'first_name': jQuery(this).find("td input[name='first_name']").val(), 
				       'last_name': jQuery(this).find("td input[name='last_name']").val(), 
				       'email': jQuery(this).find("td input[name='email']").val(),
				       'team': jQuery(this).find("td option:selected").text()
                       } // end var student
        data.push(student);
    })
    return data;
} //end get_students();

jQuery(function() {

    jQuery('#activation-btn').on('click', function(e)
    {   
    	jQuery(function()
    	{
    		
    	   	jQuery.ajax(
    	    {
    	        url: "/activate_course/" + crs_id,
    	    	type: "GET",
    	    	success: function (data) 
    	    	{
    	    		//var crs_data = data;
    	    		console.log(data);
    	    	    var data = get_students();
    	    	    console.log(data);
        	    },
	    	           
        	    error: function(data) 
	    	    {
        	        console.log("There was an error getting course details.");
	    	    }
        	}); // end ajax POST
	    }); // end inner on click function
    	e.preventDefault(); //we don't want the form submitting
	});// end on click function
});

    	            //console.log(crs_data.course[0].professor);
    	    	    //jQuery('#id_name').val(crs_data.course[0].name);
    	            //jQuery('#id_startingBudget').val(crs_data.course[0].startingBudget);
    	            //jQuery('#id_enableNarrative').val(crs_data.course[0].enableNarrative);
    	            //jQuery('#id_message').val(crs_data.course[0].message);
    	            //jQuery('#id_active').val(crs_data.course[0].active);
    	            //jQuery('#id_archive').val(crs_data.course[0].archive);
    	            //jQuery('#id_professor option:selected' ).text(crs_data.course[0].professor);
    	            

//    		
//    		
//    	    jQuery('#update-crs-btn').on('click', function(e)
//    	    {
//    	    	jQuery.ajax(
//    	        {
//    	            url: "/update_course/" + crs_id,
//    	            type: "POST",
//    	            data: {'name' : jQuery('#id_name').val(),
//    	            	   'startingBudget' : jQuery('#id_startingBudget').val(),
//    	            	   'enableNarrative' : jQuery('#id_enableNarrative').val(),
//    	            	   'message' : jQuery('#id_message').val(),
//    	            	   'active' : jQuery('#id_active').val(),
//    	            	   'archive' : jQuery('#id_archive').val(),
//    	            	   'professor' : jQuery('#id_professor option:selected' ).text()
//    	            	   },
//
//    	            success: function (data) 
//    	            {
//    	        		var crs_data = data;
//
//    	        	    jQuery('#id_name').val(crs_data.course[0].name);
//    	                jQuery('#id_startingBudget').val(crs_data.course[0].startingBudget);
//    	                jQuery('#id_enableNarrative').val(crs_data.course[0].enableNarrative);
//    	                jQuery('#id_message').val(crs_data.course[0].message);
//    	                jQuery('#id_active').val(crs_data.course[0].active);
//    	                jQuery('#id_archive').val(crs_data.course[0].archive);
//    	                jQuery('#id_professor option:selected' ).text(crs_data.course[0].professor);
//    	                
//    	            },
//    	                  
//    	            error: function(data) 
//    	            {
//    	                console.log("There was an error submitting your form.");
//    	            }
//    	          }); //end ajax UPDATE
