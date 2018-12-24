function popupOpen(fileURL) {
    var popOption = "width=380, height=350, resizable=yes, scrollbars=yes, status=yes, location=no, top=200, left=500;";
    window.open(fileURL, "", popOption);
}

$('.btnLogin').on('click', function () {
    popupOpen('/accounts/login/');
});


function openBoard(event) {
    var popOption = "width=550, height=500, resizable=yes, scrollbars=yes, status=yes, location=no, top=100, left=300;";
    window.open('/board, "", popOption);
    event.preventDefault();
    var el = event.target;
    var boardTitle = el.textContent; /*Title*/

    var dateSpan = $(el).next();
    var date = dateSpan.text(); /*Date*/

    var detailInfoEl = $(dateSpan).next();
    var detailInfo = detailInfoEl.text(); /*Content*/


}

$('#board ul li a').on('click', openBoard);
