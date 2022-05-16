  $('#clickme').click(function(){
    if (!$(this).data('status')) {
      $(this).html('');
      $(this).data('status', true);
    }
    else {
      $(this).html('Если возникли проблемы с сайтом напишите сюда');
      $(this).data('status', false);
    }
  });