$(document).ready(() => {
  $(".searchForm").submit(e => {
    e.preventDefault();
    let text = e.target.searchbar.value;
    console.log(text);
  });
});
