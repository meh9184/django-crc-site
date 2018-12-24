function popupOpen(fileURL) {
    var popOption = "width=380, height=350, resizable=yes, scrollbars=yes, status=yes, location=no, top=200, left=500;";
    window.open(fileURL, "", popOption);
}

function openBoard(event) {
    event.preventDefault();
    var el = event.target;
    $(el).addClass("activeItem");
    
    /*
    var boardTitle = el.textContent; 

    var dateSpan = $(el).next();
    var date = dateSpan.text(); 

    var detailInfoEl = $(dateSpan).next();
    var detailInfo = detailInfoEl.text();
    */
    

    var popOption = "width=550, height=500, resizable=yes, scrollbars=yes, status=yes, location=no, top=100, left=300;";
    window.open('/board', "", popOption);
    //window.open('./boardTemplate.html?title=' + boardTitle + '&date=' + date + '&detailInfo=' + detailInfo, "", popOption);
}

function openNotice(event) {
    event.preventDefault();
    var popOption = "width=550, height=500, resizable=yes, scrollbars=yes, status=yes, location=no, top=100, left=300;";
    window.open('/serviceNotice', "", popOption);
}

$('.btnLogin').on('click', function () {
    popupOpen('/accounts/login');
});

$('#board ul li a').on('click', openBoard);

$('.btnNotice').on('click',openNotice);
