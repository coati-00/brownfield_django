var saveOrderOfChildren=function(){var url="/pagetree/reorder_section_children/2/?";var worktodo=0;$("#children-order-list li").each(function(index,element){worktodo=1;var id=$(element).attr('id').split("-")[1];url+="section_id_"+index+"="+id+";";});if(worktodo==1){var req=new XMLHttpRequest();req.open("POST",url,true);req.send(null);}};var saveOrderOfPageBlocks=function(){var url="/pagetree/reorder_pageblocks/2/?";var worktodo=0;$("#edit-blocks-tab>div.block-dragger").each(function(index,element){worktodo=1;var id=$(element).attr('id').split("-")[1];url+="pageblock_id_"+index+"="+id+";";});if(worktodo==1){var req=new XMLHttpRequest();req.open("POST",url,true);req.send(null);}}
$(function(){$("#children-order-list").sortable({containment:'parent',axis:'y',tolerance:'pointer',activeClass:'dragging',handle:'.draghandle',stop:function(event,ui){saveOrderOfChildren();}});$("#children-order-list").disableSelection();$("#edit-blocks-tab").sortable({items:'div.block-dragger',axis:'y',containment:'parent',handle:'.draghandle',activeClass:'dragging',tolerance:'pointer',stop:function(event,ui){saveOrderOfPageBlocks();}});$("#edit-blocks-tab").disableSelection();});