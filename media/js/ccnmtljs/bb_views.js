/* Experimenting with suggestions from Backbone best practices for reducing duplicate code */

/* Might be good to pull out show edit form and remove */

/* All List Element Views have the same render function - creating base class with the render method. */
var BaseItemView = Backbone.View.extend({

    tagName : 'li',

    // initialize: function(options) {
    //     _.bindAll(this, 'showErrorMessage');
    //     this.error_template = _.template(jQuery("#error-message-template").html());
    // },

	  render: function () 
    {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },
    
    hideEditForm: function(e)
    {   
        e.preventDefault();
        this.render();
    },
    
    showEditForm: function(e)
    {
        var edit_form =  this.edit_form(this.model.toJSON());
        this.$el.html(edit_form);
    },

    showErrorMessage: function(selector_string, error_element, error_class, error_msg)
    {           
        var error_class = error_class.substr(1);
        var this_error_elem = this.$el.find(error_element);
        var no_b = jQuery(this_error_elem).has('b').length;
        if((no_b === 0) && ((jQuery(this_error_elem).has(error_class).length) === 0))
        {
            /* Situation 1: the error element (element we will attach/insert error message to)
            has no error message, we create and add the message to the element */
            var error_temp =  this.error_template({"error_msg": error_msg});
            jQuery(this.$el).find('.error-msg').addClass(error_class);
            jQuery(error_element).append(error_temp);
        }
        /* Situation 2: the error element (element we will attach/insert error message to)
            has an error message, but it is not for this error */
    },

    is_empty: function (selector_string, error_element, error_class, error_msg)
    {
        console.log("Inside BaseItemView is_empy");
        
        var check = jQuery(this.el).find(selector_string).val();
        if(check === null || check === "") 
        {
            this.showErrorMessage(selector_string, error_element, error_class, error_msg);
            return true;
        }
        return false;     
    },
    
    confirmArchival: function (evt)
    {
    	var current = jQuery(this.el);
    	current.find('.conf-del').show();
    	current.find('.conf-del').css({'display':'inline', 'color':'red', 'font-weight':'bold'});
    	current.find('.reg-btn').hide();
    },
    
    cancelArchive: function (evt)
    {
    	var current = jQuery(this.el);
    	current.find('.reg-btn').show();
    	current.find('.conf-del').hide();
    }

});


var DeletableItemView = BaseItemView.extend({

    removeItem: function ()
    {   
        this.model.destroy();
    }

});

/* Start with Single Element Views */


var DocumentView = BaseItemView.extend({

   	initialize: function(options) {
   	    _.bindAll(this, 'changeDocument', 'viewDocument');
   	    this.listenTo(this.model, 'change', this.render);
        this.template = _.template(jQuery("#document-list-template").html());

   	},

   	events: {
   		'click .chng-dct' : 'changeDocument',
   		'click .document-click' : 'viewDocument'
   	},
        
    changeDocument: function()
   	{
    	if(this.model.attributes.visible === true)
    	{
    		this.model.set('visible', false);
    		this.model.save({
                success: function(model, response) 
                {
                },
                error: function(model, response)
                {
                        alert("An error occured!");
                },
                wait: true
            });
    	}
    	else if (this.model.attributes.visible === false)
    	{
    		this.model.set('visible', true);
    		this.model.save({
    		        success: function(model, response) 
                    {},
                    error: function(model, response)
                    {
                            alert("An error occured!");
                    },
                    wait: true
                });
    	}
   	},
   	
   	viewDocument: function()
   	{
   		if(this.model.get('name') === "Link: Brownfield Action Reference Site")
   		{
   			document.location = "http://brownfieldref.ccnmtl.columbia.edu/";
   		}
   		else if((this.model.get('name') === "Video: Press Conference Proceedings in Moraine Township") || (this.model.get('name') === "Video: Esker County Community Television: O'Ryan's Express"))
   		{
   			window.open("../../media/" + this.model.get('link'));
   		}
   		else
		{
    		window.open("../../media/flash/" + this.model.get('link'));
		}
   	}

});


var CourseView = BaseItemView.extend({
    	
   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	    this.template = _.template(jQuery("#course-list-template").html());
   	    this.edit_form = _.template(jQuery("#course-edit-template").html());
        this.error_template = _.template(jQuery("#error-message-template").html());
   	    /* As of now cannot think of solution for having the list
   	     * of professors available to the CourseView view and the main ControlView*/
   	},
    	
   	events: {
   	    'click .course_name' : 'courseDetails',
   	    'click .edit-crs' : 'showEditForm',
   	    'click .save-edit-course' : 'editCourse',
   	    'click .cncl-edit-crs' : 'hideEditForm',
   	    'click .conf-archive-course' : 'confirmArchival',
   	    'click .cancel-arch' : 'cancelArchive',
   	    'click .conf-arch' : 'clear'
   	},
    	
    render: function ()
    {
        if (this.model.get('archive') === true) {
            this.$el.remove();
        } else {
        	BaseItemView.prototype.render.apply(this, arguments);
        }
        return this;
    },
    
    clear: function() {
        this.model.set('archive', true);
        this.model.save();
    },

    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;
        if(this.is_empty("input#edit_course_name", ".course-name-block", ".is-empty", "Please enter a valid course name."))
        {
            is_valid = false;
        }

        if(this.is_empty("input#edit_course_startingBudget", ".course-budget-block", ".is-empty", "Please enter a valid starting budget for your course."))
        {
            is_valid = false;
        }
        if(this.is_empty("textarea#edit_course_message", ".course-message-block", ".is-empty", "Please enter a valid course message."))
        {
            is_valid = false;
        }

        return is_valid;
    },
    
    editCourse: function(evt)
    {
        evt.preventDefault();
        
        if(this.validEditForm())
        {
            var name = jQuery(this.el).find("input#edit_course_name").val();
            var startingBudget = jQuery(this.el).find("input#edit_course_startingBudget").val();
            var message = jQuery(this.el).find("textarea#edit_course_message").val();

            this.model.set({'name': name, 'startingBudget': startingBudget, 'message': message});
            this.model.save({
                success: function(model, response) 
                {},
                error: function(model, response)
                {
                        alert("An error occured!");
                },
                wait: true
            });//end save
        }//end if
    },// end editCourse
    
    courseDetails: function ()
    {
        window.location.href = '/course_details/' + this.model.get('id')  + '/';  
    }
});// End CourseView


var InstructorView = BaseItemView.extend({

	initialize: function(options)
	{
		_.bindAll(this, 'editInstructor');
		this.template = _.template(jQuery("#instructor-list-template").html());
		this.edit_form =  _.template(jQuery("#instructor-edit-template").html());
        // need to bind the edit form to the model - when change made to form change model
		this.listenTo(this.model, 'change', this.render);
	},

   	events: {
   		'click .ed-inst' : 'showEditForm',
   		'click .save-edit-instructor' : 'editInstructor',
   		'click .cncl-edit-inst' : 'hideEditForm',
   		'click .conf-archive-inst' : 'confirmArchival',
   	    'click .cancel-arch-inst' : 'cancelArchive',
   	    'click .conf-arch' : 'clear'
   	},
    
    render: function ()
    {
    	var prof = this.model.get('profile');
        if (prof.archive === true) {
            this.$el.remove();
        } else {
        	BaseItemView.prototype.render.apply(this, arguments);
        }
        return this;
    },
        	
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        if(this.is_empty("input.edt-frst-name", ".inst-edt-first-name", "Please enter a first name."))
        {
            is_valid = false;
        }
        if(this.is_empty("input.edt-last-name", ".inst-edt-last-name", "Please enter a last name."))
        {
            is_valid = false;
        }
        if(this.is_empty("input.edt-email", ".inst-edt-email", "Please enter a email address."))
        {
            is_valid = false;
        }

        return is_valid;
    },

   	editInstructor: function(e)
   	{
        e.preventDefault();

        if(this.validEditForm())
        {
        	var current = jQuery(this.el);
            var inst_fname = current.find("input.edt-frst-name").val();
            var inst_lname = current.find("input.edt-last-name").val();
            var inst_email = current.find("input.edt-email").val();
            /* For some reason setting the attributes below only sets correctly if you edit
            * email, pulling the varibles here because here they are correct and then passing.
            * */
            this.model.set('first_name', inst_fname);
            this.model.set('last_name', inst_lname);
            this.model.set('email', inst_email);
            this.model.save({
	        success: function(model, response) 
	        {},
            error: function(model, response)
            {
            	alert("An error occured!");
            },
            wait: true
          });//end save
      }
    },
    
    clear: function() {
    	var prof = _.clone(this.model.get('profile'));
    	prof.archive = true;
    	this.model.set("profile", prof);
        this.model.save();
    }
    
});


var TeamView = DeletableItemView.extend({
	
   	initialize: function (options) {
   		this.template = _.template(jQuery("#team-list-template").html());
   		this.edit_form = _.template(jQuery("#team-edit-template").html());
   	    this.listenTo(this.model, 'change', this.render);
   	    this.listenTo(this.model, 'destroy', this.remove);
   	},

   	events: {
   		'click .rm-team' : 'removeItem',
   		'click .edit-team' : 'showEditForm',
   		'click .save-edit-team' : 'editTeam',
   		'click .cncl-edit-team' : 'hideEditForm',
   		'click .hist-team' : 'teamHistory'
   	},
    
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        if(this.is_empty("input.edt-team-name", ".div-edt-team-name", ".is-empty", "Please enter a team name."))
        {
            is_valid = false;
        }

        return is_valid;
    },

   	editTeam: function(e)
   	{
   		e.preventDefault();

      if(this.validEditForm())
      {
   		
   		    var first_name = jQuery(this.el).find("input.edt-team-name").val();
   		
  		    this.model.set('first_name', first_name);
   		        this.model.save({
	            success: function(model, response) 
	            {},
            error: function(model, response)
            {
            	alert("An error occured!");
            },
            wait: true
            });//end save
      }
    },
    
   	teamHistory: function()
   	{
   		window.open("../../team_csv/" + this.model.get('username') + '/');
   	}
});// End Team View


var StudentView = DeletableItemView.extend({

	initialize: function(options)
	{
		_.bindAll(this, 'editStudent', 'hideEditForm', 'showEditForm');
		this.template = _.template(jQuery("#student-list-template").html());
		this.edit_form = _.template(jQuery("#student-edit-template").html());
		this.listenTo(this.model, 'change', this.render);
		this.listenTo(this.model, 'destroy', this.remove);
	},

   	events: {
   		'click .ed-st' : 'showEditForm',
   		'click .save-edit-student' : 'editStudent',
   		'click .cncl-edit-std' : 'hideEditForm',
   		'click .rm-st' : 'removeItem'
   	},
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        if(this.is_empty("input.edt-frst-name", ".sedt-first-name", ".is-empty", "Please enter a first name."))
        {
            is_valid = false;
        }

        if(this.is_empty("input.edt-last-name", ".sedt-last-name", ".is-empty", "Please enter a last name."))
        {
            is_valid = false;
        }
        if(this.is_empty("input.edt-email", ".sedt-email", ".is-empty", "Please enter a email address."))
        {
            is_valid = false;
        }

        return is_valid;
    },
   	editStudent: function(e)
   	{
   		e.preventDefault();

      if(this.validEditForm())
      {
          var std_fname = jQuery(this.el).find("input.edt-frst-name").val();
          var std_lname = jQuery(this.el).find("input.edt-last-name").val();
          var std_email = jQuery(this.el).find("input.edt-email").val();
          /* For some reason setting the attributes below only sets correctly if you edit
          * email, pulling the varibles here because here they are correct and then passing.
          * */
          this.model.set('first_name', std_fname);
          this.model.set('last_name', std_lname);
          this.model.set('email', std_email);
          this.model.save({
          success: function(model, response) 
          {},
          error: function(model, response)
          {
              alert("An error occured!");
          },
          wait: true
        });//end save
      }
    }

});


var InstructorView = DeletableItemView.extend({

	initialize: function(options)
	{
		_.bindAll(this, 'editInstructor');
		this.template = _.template(jQuery("#instructor-list-template").html());
		this.edit_form =  _.template(jQuery("#instructor-edit-template").html());
        // need to bind the edit form to the model - when change made to form change model
		this.listenTo(this.model, 'change', this.render);
		this.listenTo(this.model, 'destroy', this.remove);
	},

   	events: {
   		'click .ed-inst' : 'showEditForm',
   		'click .save-edit-instructor' : 'editInstructor',
   		'click .cncl-edit-inst' : 'hideEditForm',
   		'click .rm-inst' : 'removeItem'
   	},
    
    validEditForm: function(attributes, options) {
        /* Extremely simple basic check. */
        var is_valid = true;

        if(this.is_empty("input.edt-frst-name", ".inst-edt-first-name", ".is-empty", "Please enter a first name."))
        {
            is_valid = false;
        }

        if(this.is_empty("input.edt-last-name", ".inst-edt-last-name", ".is-empty", "Please enter a last name."))
        {
            is_valid = false;
        }
        if(this.is_empty("input.edt-email", ".inst-edt-email", ".is-empty", "Please enter a email address."))
        {
            is_valid = false;
        }

        return is_valid;
    },

   	editInstructor: function(e)
   	{
        e.preventDefault();

        if(this.validEditForm())
        {
            var inst_fname = jQuery(this.el).find("input.edt-frst-name").val();
            var inst_lname = jQuery(this.el).find("input.edt-last-name").val();
            var inst_email = jQuery(this.el).find("input.edt-email").val();
            /* For some reason setting the attributes below only sets correctly if you edit
            * email, pulling the varibles here because here they are correct and then passing.
            * */
            this.model.set({'first_name': inst_fname,
                            'last_name': inst_lname,
                            'email': inst_email});
            this.model.save({
	        success: function(model, response) 
	        {},
            error: function(model, response)
            {
            	alert("An error occured!");
            },
            wait: true
          });//end save
      }
    }
    
});


/* Now the Collection Views */
var BaseListView = Backbone.View.extend({

    renderCollection: function() {
        this.collection.each(function(model)
        {
            this.$el.append(new this.item_view({
                model: model
            }).render().el);
        }, this);
        return this;
    },
    
    addItem: function(model, collection, options)
    {
        this.$el.append(new this.item_view({
            model: model
        }).render().el);
    }

});

var InstructorListView = BaseListView.extend({
    
    initialize: function (options)
    {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new InstructorCollection(options);
        this.collection.fetch({processData: true, reset: true});
        this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.item_view = InstructorView;
    }
});


var CourseListView = BaseListView.extend({
    
    initialize: function (options)
    {
    	_.bindAll(this, 'renderCollection', 'addItem');
    	this.collection = new CourseCollection(options);
    	this.collection.fetch({processData: true, reset: true});
    	this.collection.on('reset', this.renderCollection);
    	this.collection.on('add', this.addItem);
    	this.item_view = CourseView;
	}

});


var DocumentListView = BaseListView.extend({

    initialize: function (options)
    {
        _.bindAll(this, 'renderCollection');
  	
  	    this.collection = new DocumentCollection(options);
  	    this.collection.fetch({processData: true, reset: true});
  	    this.collection.on('reset', this.renderCollection);
  	    this.item_view = DocumentView;
	}
});


var StudentListView = BaseListView.extend({

    initialize: function (options)
    {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new StudentCollection(options);
        this.collection.fetch({processData: true, reset: true});
        this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.item_view = StudentView;
	}
    
});


var TeamListView = BaseListView.extend({

    initialize: function (options)
    {
        _.bindAll(this, 'renderCollection', 'addItem');
        this.collection = new TeamCollection(options);
        this.collection.fetch({processData: true, reset: true});
    	this.collection.on('reset', this.renderCollection);
        this.collection.on('add', this.addItem);
        this.item_view = TeamView;
	}
    
});



