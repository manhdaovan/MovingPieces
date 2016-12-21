function chooseThis(ele) {
    ele.toggleClass("choosing");
}

function checkMove(vertical) {
    var allChoosingElements = $(".choosing");
    if (allChoosingElements.length > 2) {
        alert("allChoosingElements.length > 2");
        clearAllChoosing();
        return;
    }

    if (allChoosingElements.length == 2) {
        if (!allChoosingElements.hasClass("first_item")) {
            alert("Please choose blank piece to move");
            clearAllChoosing();
            return;
        }
        move(allChoosingElements[0], allChoosingElements[1], vertical);
        clearAllChoosing();
    }
}

function clearAllChoosing() {
    $(".item, .first_item").removeClass("choosing");
}

function move(e1, e2, vertical) {
    var e1_id = parseInt($(e1).data("id"), 10);
    var e2_id = parseInt($(e2).data("id"), 10);
    var arrMovableIds = [e1_id - vertical, e1_id + vertical, e1_id - 1, e1_id + 1]; //Upper, lower, left, right
    if (arrMovableIds.indexOf(e2_id) >= 0) {
        swap(e1, e2);
    } else {
        alert("Unmovable");
    }
}

function swap(e1, e2) {
    var tmpClassE1 = $(e1).attr("class");
    var tmpClassE2 = $(e2).attr("class");

    var tmpE1HTMl = $(e1).html();
    var tmpE2HTMl = $(e2).html();

    $(e1).removeClass(tmpClassE1);
    $(e1).addClass(tmpClassE2);

    $(e2).removeClass(tmpClassE2);
    $(e2).addClass(tmpClassE1);

    $(e1).html(tmpE2HTMl);
    $(e2).html(tmpE1HTMl);
}
