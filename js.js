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

});
