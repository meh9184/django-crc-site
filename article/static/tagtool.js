/**
 * Created by Jung Geunseong on 2016-0623(023).
 */

// Change This!
var tagTool = {
    mainTextBlock: "#newsbodytext",
    selectedTextBlock: "#copied-p",
    selectedWordpart: ".subject"
};

var insertingRow = ".inserting";

if (!window.Tagtool) {
    Tagtool = {};
}

Tagtool.Selector = {};
Tagtool.Selector.getSelected = function () {
    var t = '';
    if (window.getSelection) {
        t = window.getSelection();
    } else if (document.getSelection) {
        t = document.getSelection();
    } else if (document.selection) {
        t = document.selection.createRange().text;
    }
    return t;
}

// 메인 텍스트가 드래그 되었을 때 
Tagtool.Selector.mouseupMaintext = function () {
    var st = Tagtool.Selector.getSelected();
    if (st != '') {
        $("#copied-p").text(st);
        $(".sentence>span", insertingRow).text(st);
    }
}


// 선택된 텍스트에서 다시 드래그 되었을 때
Tagtool.Selector.mouseupSelected = function () {
    Tagtool.tablecursor = 1;
    var st = Tagtool.Selector.getSelected();
    if (st != '') {
        $(tagTool.selectedWordpart,insertingRow).val(st);
		
    }
}



// 실행 부분
// 문장 선택 이벤트
$(document).ready(function(){
$(tagTool.mainTextBlock).bind("mouseup", Tagtool.Selector.mouseupMaintext);
$(tagTool.selectedTextBlock).bind("mouseup", Tagtool.Selector.mouseupSelected);
                

// 워드파트 이벤트
$("input[name=wordpart]:radio").change(function () {
                                       console.log('radio', $(this).val());
    tagTool.selectedWordpart = "." + $(this).val();
});
    


// 행추가 이벤트, 각 행 버튼의 이벤트를 추가한다
var rowTemplate = $(".inserting").clone();

var oldname = "old";
$("button[name=addRow]").click(function () {
    var savingRow = $("tbody tr:first-child");
    // 문장 저장
    $('.sentence span', savingRow).text($(tagTool.selectedTextBlock).text());
    savingRow.removeClass("inserting");
	
	//행추가시 라이디오버튼 중복 처리		
	oldname += "d";
	$("input[name=newsub]").prop("name", oldname+"s");
	$("input[name=newobj]").prop("name", oldname+"o");
	$("input[name=newverb]").prop("name", oldname+"v");
	$("input[name=newetc]").prop("name", oldname+"e");
	$("input[name=newpassive]").prop("name", oldname+"p");


    $("tbody").prepend(rowTemplate.clone());

    $("button[name=deleteRow]", savingRow).click(function () {
        console.log("삭제: ", $(this).parents("tr").html());

        $(this).parents("tr").remove()
    });

    $("button[name=viewSentence]", savingRow).click(function () {
        alert($("span", $(this).parent()).text());
    });
});


// 송신 이벤트
$("button[name=saveServer]").click(function () {
    var sendingRow = {
        aid: $('#aid').val(),
        subject: '',
        object: '',
        verb: '',
        sentence: '',
        title: '',
		aetc: '',
		subjectflag: '',
		objectflag: '',
		verbflag: '',
		etcflag: '',
		passiveflag: ''
    };

    $("#wordpartTable tbody tr").each(function () {
			if ($('.subject', this).val() != "" && $('.object', this).val() != "" && $('.verb', this).val() != "" && $(':radio[class="subjectflag"]:checked', this).val()!=undefined && $(':radio[class="objectflag"]:checked', this).val()!=undefined && $(':radio[class="verbflag"]:checked', this).val()!=undefined && $(':radio[class="passiveflag"]:checked', this).val()!=undefined){

        sendingRow = new SendingRow(
            $('.subject', this).val(),
            $('.object', this).val(),
            $('.verb', this).val(),
            $('.sentence span', this).text(),
			$('.aetc', this).val(),
			$(':radio[class="subjectflag"]:checked', this).val(),
			$(':radio[class="objectflag"]:checked', this).val(),
			$(':radio[class="verbflag"]:checked', this).val(),
			$(':radio[class="etcflag"]:checked', this).val(),
			$(':radio[class="passiveflag"]:checked', this).val()
        );

        console.log(sendingRow);

        $.ajax({
            type: 'POST',
            url: 'saveTags',
            data: sendingRow,
            success: function (resp) {
               console.log(resp);
				alert(resp);
            }

        });
	} else {
		$("#statusMessage").text("저장 실패: 필수 요소를 선택또는 입력해주세요!");
		alert("Warning: Fill out the requirements!");
		}

    });

});
                  
                    });

function SendingRow(sub, obj, verb, st, etc, subflag, obflag, vbflag, etflag, passflag) {
    var sendingRow = {
        aid: $('#aid').val(),
        subject: sub,
        object: obj,
        verb: verb,
        sentence: st,
		aetc: etc,
		subjectflag: subflag,
		objectflag: obflag,
		verbflag: vbflag,
		etcflag: etflag,
		passiveflag: passflag,
        title: $("#atitle").text()
    };

    return sendingRow;
}
