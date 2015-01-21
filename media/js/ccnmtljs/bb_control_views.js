var BaseManagementView = Backbone.View.extend({

    showAddItemForm: function(e)
    {
        
    },
    
    hideAddItemForm: function(e)
    {
        
    }
    
});

var ManageCoursesView = Backbone.View.extend({
    events: {
    	'click .add-crs': 'showCourseForm',
    	'click .cncl-add-crs' : 'hideAddForm',
    	'click .submit': 'addCourse'
    },
    
    initialize: function (options) {
        _.bindAll(this,
                  'addCourse',
                  'showCourseForm',
                  'hideAddForm',
                  'validateForm');

        this.options = options;
        this.course_list_view = new CourseListView({el: this.options.listEl});
        this.course_list_view.collection.fetch({wait: true});
        this.user_list = new InstructorCollection();
        this.user_list.fetch({wait: true});
    },

    showCourseForm: function(e) {
		jQuery(".add-crs").hide();
		//how to bind this/make it wait for results from server
		this.user_list.fetch({wait: true});
		this.user_list.each(function(model) {
	        jQuery('#id_professor').append("<option value='" + String(model.attributes.url) + "'>" + 
	                String(model.attributes.first_name) + 
	                " " + String(model.attributes.last_name)  + 
	                "</option>");
	    });
		jQuery("#create-course-form").show();
    },
    
    hideAddForm: function()
    {   
    	this.$('#create-course-form').css('display', 'none');
    	jQuery(".add-crs").show();
    },
    
    validateForm: function()
    {
        var is_valid = true;
        
        var course_name = jQuery('#id_course_name').val();
        var startingBudget = jQuery('#id_course_startingBudget').val();
        var course_message = jQuery('#id_course_message').val();
        
        if(course_name === null || course_name === "")
        {   
            jQuery('.course-name-block').append("<p style='color:#ff0000'>Please enter a valid course name.</p>");
            is_valid = false;
        }
        if(startingBudget === null || startingBudget === "")
        {   
            jQuery('.course-budget-block').append("<p style='color:#ff0000'>Please enter a valid starting budget for your course.</p>");
            is_valid = false;
        }
        if(course_message === null || course_message === "")
        {   
            jQuery('.course-message-block').append("<p style='color:#ff0000'>Please enter a valid course message.</p>");
            is_valid = false;
        }
        return is_valid;
    },

    addCourse: function(evt) {
        evt.preventDefault();
        
        var professor = jQuery('#id_professor').find("option:selected").val();

        if(professor === null || professor === undefined)
        {   
            professor = this.user.get('url');
        }

        if (this.validateForm())
        {
    	    this.course_list_view.collection.create({
    	        name: jQuery("#id_course_name").val(),
    	    	startingBudget: jQuery("#id_course_startingBudget").val(),
    	    	message: jQuery("#id_course_message").val(),
    		    professor: professor
    	    }, {wait: true});

    	    jQuery("#create-course-form").hide();
    	    jQuery(".add-crs").show();
        }
	    return false;
    }
});// End UserControlView  


var ManageInstructorsView = Backbone.View.extend({
    events: {
    	'click .add-instructor-btn': 'showInstructorForm',
    	'click .cncl-add-inst' : 'hideAddForm',
    	'click .save-instructor': 'addInstructor'
    },
    
    initialize: function (options) {
        _.bindAll(this,
                  'addInstructor',
                  'showInstructorForm',
                  'onlyLetters');
        this.instructor_collection_view = new InstructorListView({
            el: jQuery('.instructor-list'),
        });
    },

    showInstructorForm: function(e) {
		jQuery(".add-instructor-btn").hide();
		jQuery(".add-instructor-frm").show();
    },
    
    hideAddForm: function()
    {   
    	this.$('.add-instructor-frm').css('display', 'none');
    	jQuery(".add-instructor-btn").show();
    },
    
    onlyLetters: function (check_string){
    	alert(check_string);
        //var TCode = document.getElementById('TCode').value;
        if( /[^a-zA-Z0-9]/.test( check_string ) ) {
           alert('Please only enter letters for first and last names');
           return false;
        }
        return true;     
     },

    addInstructor: function(evt) {
    	//evt.stopPropagation();
    	this.instructor_collection_view.collection.create(
    		{
    		    first_name : jQuery(".instructor-frst-name").val(),
    		    last_name : jQuery(".instructor-last-name").val(),
    		    email : jQuery(".instructor-email").val()
    	    },
    	    {
    	    	error: function(model, response)
                {
                	jQuery(".add-instructor-frm").append("<p>Something went wrong, please try again.</p>");
                },
    	    	wait: true
    	    });

	    jQuery(".add-instructor-frm").hide();
	    jQuery(".add-instructor-btn").show();
  	    return false;
    },
    
    validateInstructorForm: function(e) {
    	e.stopPropagation();
    	
    	if((jQuery(".add-instructor-frm input.instructor-frst-name").val().length) === 0)
    	{
    		if((jQuery(".inst-first-name").has('b').length) === 0)
    		{
    			jQuery(".inst-first-name").append("<b>Please enter a first name.</b>").css('color', 'red');
    		}
    	}
    	if((jQuery(".add-instructor-frm input.instructor-last-name").val().length) === 0)
    	{
    		if((jQuery(".inst-last-name").has('b').length) === 0)
    		{
    			jQuery(".inst-last-name").append("<b>Please enter a last name.</b>").css('color', 'red');
    		}
    	}
    	if((jQuery(".add-instructor-frm input.instructor-email").val().length) === 0)
    	{
    		if((jQuery(".inst-email").has('b').length) === 0)
    		{
    			jQuery(".inst-email").append("<b>Please enter a email.</b>").css('color', 'red');
    		}
    	}
    	//check whatever they put for email looks something like an actual address
    	else if((jQuery(".add-instructor-frm input.instructor-email").val().length) !== 0)
    	{
    	    if((jQuery(".add-instructor-frm input.instructor-email").val().indexOf("@")  === -1) && 
    	       (jQuery(".add-instructor-frm input.instructor-email").val().indexOf(".") === -1))
    	    {
    		    if((jQuery(".inst-email").has('b').length) === 0)
    		    {
    			    jQuery(".inst-email").append("<b>Please enter a valid email.</b>").css('color', 'red');
    		    }
    	    }
    	}
    	//if above tests pass reasonable to submit
    	this.addInstructor();
    }
    
});  


var StudentControlView = Backbone.View.extend({

    events: {
	'click .add-std-btn' : 'showStudentForm',
	'click .cncl-add-std' : 'hideAddForm',
	'click .student_submit' :	'validateStudentForm'
    },
    
    initialize: function (options)
    {
    	_.bindAll(this, 'addStudent', 'hideAddForm', 'validateStudentForm');
        this.student_collection_view = new StudentListView({
            el: jQuery('.student-list'),
            course: options.course
        });
    },

    showStudentForm: function() {
		jQuery(".add-std-btn").hide();
		jQuery(".add-std-frm-title").show();
		jQuery(".add-std-frm").show();
    },
    
    hideAddForm: function(e) {
    	this.$('.add-std-frm-title').css('display', 'none');
    	this.$('.add-std-frm').css('display', 'none');
    	jQuery(".add-std-btn").show();
    },
    
    addStudent: function(e) {
    	
    	this.student_collection_view.collection.create(
    	    {   
    	        	first_name : jQuery(".frst-name").val(),
    	            last_name : jQuery(".last-name").val(),
    	            email : jQuery(".email").val()
    	    },
    	    {
                error: function(model, response)
                {
                	jQuery(".add-team-frm").append("<p>Something went wrong, please try again.</p>");
                },
    	        wait: true,
    	    	url: this.student_collection_view.collection.url()
    	    }
    	);
	    jQuery(".add-std-frm-title").hide();
	    jQuery(".add-std-frm").hide();
	    jQuery(".add-std-btn").show();
	    return false;
    },
    
    
    validateStudentForm: function(e) {
    	e.preventDefault();
    	
    	//there is probably a better way to do this... should also be it's own method like checkBlank
    	if((jQuery(".add-std-frm input.frst-name").val().length) === 0)
    	{
    		if((jQuery(".first-name-box").has('b').length) === 0)
    		{
    			jQuery(".first-name-box").append("<b>Please enter a first name.</b>").css('color', 'red');
    		}
    	}
    	if((jQuery(".add-std-frm input.last-name").val().length) === 0)
    	{
    		if((jQuery(".last-name-box").has('b').length) === 0)
    		{
    			jQuery(".last-name-box").append("<b>Please enter a last name.</b>").css('color', 'red');
    		}
    	}
    	if((jQuery(".add-std-frm input.email").val().length) === 0)
    	{
    		if((jQuery(".email-box").has('b').length) === 0)
    		{
    			jQuery(".email-box").append("<b>Please enter a email.</b>").css('color', 'red');
    		}
    	}
    	//check whatever they put for email looks something like an actual address
    	else if((jQuery(".add-std-frm input.email").val().length) !== 0)
    	{
    	    if((jQuery(".add-std-frm input.email").val().indexOf("@")  === -1) && 
    	       (jQuery(".add-std-frm input.email").val().indexOf(".") === -1))
    	    {
    		    if((jQuery(".email-box").has('b').length) === 0)
    		    {
    			    jQuery(".email-box").append("<b>Please enter a valid email.</b>").css('color', 'red');
    		    }
    	    }
    	}
    	//if above tests pass reasonable to submit
    	this.addStudent();
    }
    
});


var TeamControlView = Backbone.View.extend({

    events: {
	'click .add-team-btn' : 'showTeamForm',
	'click .cncl-add-team' : 'hideAddForm',
	'click .team_submit' :	'addTeam'
    },
    
    initialize: function (options) {
        this.team_collection_view = new TeamListView({
            el: jQuery('.team-list'),
            course: options.course
        });
    },

    showTeamForm: function() {
		jQuery(".add-team-btn").hide();
		jQuery(".add-team-frm-title").show();
		jQuery(".add-team-frm").show();
    },
    
    hideAddForm: function(e) {
    	this.$('.add-team-frm-title').css('display', 'none');
    	this.$('.add-team-frm').css('display', 'none');
    	jQuery(".add-team-btn").show();
    },

    addTeam: function(team) {
    	team.preventDefault();
    	this.team_collection_view.collection.create(
    	{
    		team_name : jQuery(".team-name").val()
    	},
	    {
    	    success: function(model, response) 
    	    {
            },
            error: function(model, response) {
            	jQuery(".add-team-frm").append("<p>Something went wrong, please try again.</p>");
            },
	        wait: true,
	    	url: this.team_collection_view.collection.url()
	    }
    	);
	    jQuery(".add-team-frm-title").hide();
	    jQuery(".add-team-frm").hide();
	    jQuery(".add-team-btn").show();
	    return false;
    },
    
    showError: function() {
    },
    
    showSuccess: function() {
    }
    
});// End TeamControlView  





