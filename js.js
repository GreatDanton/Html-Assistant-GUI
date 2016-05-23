$(document).ready(function() {
  $("#back-to-top").click(function(){
    $('html, body').animate({
      scrollTop: 0}, 'medium');
  });

  $('.doc-link').click(function(){
    var id = $(this).attr('id');
    id = id.replace('-link', '');
    $('html, body').animate({
      scrollTop: $('#' + id).offset().top - 70}, 'medium');
    });

  $('.icon-menu').click(function() {
    if ($('.mobile-modal').hasClass('mobile-modal-visible')) {
      $('.mobile-modal').removeClass('mobile-modal-visible');
    } else {
      $('.mobile-modal').addClass('mobile-modal-visible');
    }
  });

  var nav_top;
  nav_top = $('.nav-container').offset().top;

  if ($(window).scrollTop() > nav_top) {
    $('.navigation').addClass('nav-box-shadow');
    $('.navigation').css('position', 'fixed');
    $('.mobile-modal').css('position', 'fixed');
  }

	$(document).on("scroll", function() {
    // if viewport is below nav_top add fixed position to navigation
		if ($(window).scrollTop() > nav_top) {
      $('.navigation').addClass('nav-box-shadow');
      $('.navigation').css('position', 'fixed');
      $('.mobile-modal').css('position', 'fixed');
		} else {
			$('.navigation').removeClass('nav-box-shadow');
      $('.navigation').css('position', 'static');
      $('.mobile-modal').css('position', 'absolute');
		}
	});

});
