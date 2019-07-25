$(document).ready(function() {
	stepper1 = new Stepper($('.bs-stepper')[0])
	$('.sidebar-menu').tree()
	// $('body').bootstrapMaterialDesign();
	$('.fixed-action-btn').click(function(){
		console.log("i am in")
	})
})
