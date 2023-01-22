
$('#send').on('click', function() {
  const url_value = $('#url_value').val()
  $('#loader').removeClass('hidden');
  $('#url_value').removeClass('error_msg');

  $("ul").empty();
  $.ajax({
    url: '/crawlers/',
    data: { url: url_value },
    method: 'POST',
  })
  .done((res) => {
    getStatus(res.task_id);
  })
  .fail((err) => {
    console.log(err);
  });
});

function getStatus(taskID) {
  $.ajax({
    url: `/crawlers/${taskID}/`,
    method: 'GET'
  })
  .done((res) => {
    const taskStatus = res.task_status;
    if (taskStatus === 'SUCCESS') {
      res.task_result.map(function(item){
        $("ul").append(`<li>${item}</li>`);
      })
    }

    if (taskStatus === 'FAILURE') {
      $('#url_value').addClass('error_msg');
    }
    if (taskStatus === 'FAILURE' || taskStatus === 'SUCCESS') {
      $('#loader').addClass('hidden');
      return false;
    }
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  });
}
