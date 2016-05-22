$(document).ready(function() {
  $("#back-to-top").click(function(){
    $('html, body').animate({
      scrollTop: 0}, 'medium');
  });

  $('.doc-link').click(function(){
    var id = $(this).attr('id');
    id = id.replace('-link', '');
    $('html, body').animate({
      scrollTop: $('#' + id).offset().top - 40}, 'medium');
    });

  $('.icon-menu').click(function() {
    if ($('.mobile-modal').hasClass('mobile-modal-visible')) {
      $('.mobile-modal').removeClass('mobile-modal-visible');
    } else {
      $('.mobile-modal').addClass('mobile-modal-visible');
    }
  });

  var nav_top;

  if ($('.mobile').is(':hidden')) {
    nav_top = $('.navigation').offset().top;
  } else {
    nav_top = $('.mobile').offset().top;
  }

	$(document).on("scroll", function() {
    // magic number, navigation 160px from top
		if ($('.navigation').offset().top > nav_top) {
      // console.log($('.navigation').offset().top);
      $('.navigation').addClass('nav-box-shadow');
		} else {
			$('.navigation').removeClass('nav-box-shadow');
		}
	});

});
