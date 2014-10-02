var Document = Backbone.Model.extend({

    urlRoot: '/document/',
    
    defaults: function() {
        return {
        	id: 0,
            name: "Default Document",
            course: "Default Doc Course",
            link: "",
            visible : false
        }
    },

    initialize: function(attributes) 
	{   
	    this.name = attributes.name || '<EMPTY>'; 
	}
	    
});

var crs_id = jQuery(".crs-activate input[name='crs-id']").val();

var DocumentCollection = Backbone.Collection.extend({
	 model: Document,
	 url: function() {
		    return '/document/' + crs_id;
	  }
		 
});
// End of Models/Collections


// Views 
var DocumentView = Backbone.View.extend({

   	tagName : 'li',
   	template: _.template("Document Template <%= name %>" +
   			             "<%= link %> " +
   			             "Visibility of Document: " +
   			             "<%= visible %> " +
   			             "<button class='btn btn-xs chng-dct'>" +
   			             "Release/Revoke Document" +
   			             "</button>"),

   	initialize: function () {
   	    this.listenTo(this.model, 'change', this.render);
   	},

   	events: {
   		'click .chng-dct' : 'changeDocument'
   	},

    render: function () {
        if (!this.model) 
        {
            throw "Model is not set for this view";
        }
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },
        
    changeDocument: function()
   	{   
    	/*Can't figure out how to use backbone without getting authentication errors...*/
    	//console.log("Releasing Document");
        this.model.save(
        	{
        	wait:true,
        	//success:function(model, response) {
        	success: function(response) {
        	        console.log('Successfully saved!');
        	},
        	//error: function(model, error) {
        	error: function(response) {
                //console.log(model.toJSON());
                console.log('error.responseText');
            }
        });// end model save
   	}

});// End DocumentView


/* Container to hold rows of documents */
var DocumentListView = Backbone.View.extend({

    tagName : 'ul',

    initialize: function (options)
    {
    	_.bindAll(this,
    			 'render',
    			 'initialRender');
    	console.log(crs_id);
    	//create new collection to hold course documents
    	this.course_document_collection = new DocumentCollection();
    	this.course_document_collection.fetch({processData: true, reset: true});
    	this.course_document_collection.on('reset', this.initialRender);
	},

    render: function() {
    },

    initialRender: function() {

        this.$el.empty();

        this.course_document_collection.each(function(model) {
        this.$el.append(new DocumentView({
               model: model
        }).render().el);
        }, this);

        return this;
    }
    
});// End DocumentListView    



var document_collection_view = new DocumentListView({el : jQuery('.documents_list')});

// connecting the views to the html/page
//jQuery('.documents_list').append(document_collection_view.render().el);

//jQuery("#good_con input[name='conversation']").val();.course-activation .crs-activate 
//jQuery('#activation-btn').click(console.log("button clicked"));
//'click',
//    function(){
//        console.log("you clicked on the button");
//});


//        this.activationForm = this.$(".crs-activate");
//	    this.activationButton = this.$(".crs-activate .btn btn-mini btn-success");
//	    
//	    this.activationButton.on('click', this.activateCourse);
