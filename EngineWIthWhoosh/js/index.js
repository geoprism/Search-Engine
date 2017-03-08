$(document).ready(() => {
  $(".searchForm").submit(e => {
    e.preventDefault();
    let text = e.target.searchbar.value;
      $(".results-container").empty();
      animate();
      $.get("https://search-engine-tornado.herokuapp.com/search/api/"+text, function(data){
        fillResults(data);
      });
  });
});

function fillResults(data){
  let result = "";
  for(let i=0; i<data.content.length; i++){
    let url = data.content[i].url;
    if(url.length > 70)
      url = url.substring(0,70) + "...";
    result += "<a href=https://" + data.content[i].url + "><span class='title'>" + data.content[i].title + "</span></a>\n";
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
