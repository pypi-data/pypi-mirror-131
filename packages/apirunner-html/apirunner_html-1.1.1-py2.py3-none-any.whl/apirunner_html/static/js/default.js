
output_list = Array();
/* level - 0:Summary; 1:Failed; 2:error; 3:skip; 4:pass; 5:all*/

function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;

        if (level === 0 && tr.getAttribute('type') === 'case') {
            tr.className = '';
        } else if (level === 1) {
            if (id.indexOf('testfail') === 0) {
                tr.className = '';
            } else if (tr.getAttribute('type') === 'case') {
                tr.className = 'hiddenRow';
            }
        } else if (level === 2) {
            if (id.indexOf('testerror') === 0) {
                tr.className = '';
            } else if (tr.getAttribute('type') === 'case') {
                tr.className = 'hiddenRow';
            }
        } else if (level === 3) {
            if (id.indexOf('testskip') === 0) {
                tr.className = '';
            } else if (tr.getAttribute('type') === 'case') {
                tr.className = 'hiddenRow';
            }
        } else if (level === 4 ) {
             if (id.indexOf('testpass') === 0) {
                tr.className = '';
            } else if (tr.getAttribute('type') === 'case') {
                tr.className = 'hiddenRow';
            }
        } else if (tr.getAttribute('type') === 'case') {
            tr.className = '';
        }
    }
}
/*
function showAllClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    divs = document.getElementsByTagName("div");
    if (document.getElementById(cid).innerText.substr(0,4) == '查看详情') {
        document.getElementById(cid).innerText = "关闭详情"
        for (var a = 0; a < divs.length; a++){
            div = divs[a];
            id = div.id;
            if (id != null && typeof(id)!="undefined" ){
                if (id.substr(0,3) == 'div') {
                    document.getElementById(id).style.display = 'block';
                }
            }
        }
    }
    else {
        document.getElementById(cid).innerText = "查看详情"
        for (var a = 0; a < divs.length; a++){
            div = divs[a];
            id = div.id;
            if (id != null && typeof(id)!="undefined" ){
                if (id.substr(0,3) == 'div') {
                    document.getElementById(id).style.display = 'none';
                }
            }
        }
    }
}
*/
/* 全部的用例展开折叠div_*/
function showAllClassDetail(cid, count) {
    trs = document.getElementsByTagName("tr");
    if (document.getElementById(cid).innerText == '查看详情') {
        document.getElementById(cid).innerText = "关闭详情";
        for (var i = 0; i < trs.length; i++) {
            tr = trs[i];
            tr_id = tr.id;
            className = tr.className
            if ((className == '' || typeof(className)=="undefined")&& tr_id.substr(0,4) == 'test'){
                 var tds = tr.getElementsByTagName('td');
                 div = tds[1].getElementsByClassName('popup_window');
                 td_id = div[0].id;
                 if (td_id.indexOf(tr_id)){
                     document.getElementById(td_id).style.display = 'block';
                 }
            }
        }
    }
    else {
        document.getElementById(cid).innerText = "查看详情";
        for (var i = 0; i < trs.length; i++) {
            tr = trs[i];
            tr_id = tr.id;
            className = tr.className
            if ((className == '' || typeof(className)=="undefined")&& tr_id.substr(0,4) == 'test'){
                 var tds = tr.getElementsByTagName('td');
                 div = tds[1].getElementsByClassName('popup_window');
                 td_id = div[0].id;
                 if (td_id.indexOf(tr_id)){
                     document.getElementById(td_id).style.display = 'none';
                 }
            }
        }
    }
}


function showClassDetail(cid, count) {
    var tr_list = document.querySelectorAll('tr[cid='+cid+']');
    var toHide = 1;

    for (var i = 0; i < count; i++) {
        if (tr_list[i].className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        if (toHide) {
            tr_list[i].className = 'hiddenRow';
        } else {
            tr_list[i].className = '';
        }
    }
    return toHide
}

function showTestDetail(div_id){
    var details_div = document.getElementById(div_id);
    var displayState = details_div.style.display;
    if (displayState !== 'block' ) {
        details_div.style.display = 'block';
    } else {
        details_div.style.display = 'none';
    }
}
function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}


