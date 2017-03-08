$(document).ready(() => {
  $(".searchForm").submit(e => {
    e.preventDefault();
    let text = e.target.searchbar.value;
      $(".results-container").empty();
      animate();

      $.ajax({
        type:"GET",
        url:"http://localhost:5000/search/api/" + text,
        success:function(data){
          fillResults(data);
        },
        error:function(data){
          alert(data);
        }
      });
  });
});

function fillResults(data){
  let result = "";
  for(let i=0; i<data.content.length; i++){
    let url = data.content[i].url;
    let title = data.content[i].title;
    if(url.length > 70)
      url = url.substring(0,70) + "...";
    if(title.length > 60)
      title = title.substring(0,60) + "...";
    result += "<a href=https://" + data.content[i].url + "><span class='title'>" + title + "</span></a>\n";
    result += "<p><span class='link'>" + url + "</span><br>";
    result += data.content[i].description + "</p>";
  }
  $(".results-container").append(result);
}


function animate(){
  $('.main-title').animate({
    marginTop:'2%'
  });
  $('.search-container').animate({
    marginTop:'20px'
  });
}
