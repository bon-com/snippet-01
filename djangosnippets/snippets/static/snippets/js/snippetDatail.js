"use strict";

/** スニペット削除URL */
var DELETE_COMMENT_URL = "/snippets/comments/delete/id/";
/** テーブル背景色 */
$("table td").css("background-color", "#f8f8f8");

/** オンロードイベント */
$(function () {
  // スニペットのカテゴリ
  let key = $("#category-id").text()
  $("#category-id").text(CATEGORYS[key])

  // コメントのカテゴリ
  $(".comment_category").each((i, e) => {
    let val = $(e).text()
    $(e).text(CATEGORYS[val])
  });
});


/** コメント削除モーダル表示イベント */
$(document).on("click", ".btn-delete", function(e) {
  // これを記述しないとaタグのhref属性「#」が優先されてイベントが発火しない
  e.preventDefault(); 
  // モーダル情報セット
  let sId = $(e.target.closest(".comment-info")).find("input[name=itemId]").val();
  $("#delete-id").val(sId);
  let sName = $(e.target.closest(".comment-info")).find("input[name=itemName]").val();
  $("#delete-title").text(sName);

  // モーダル表示
  var myModal = new bootstrap.Modal($("#myModal"));
  myModal.show();
});

/** モーダル閉じるイベント */
$(document).on("click", ".modal-close", function(e) {
  $(".modal-backdrop").hide();
});

/** コメント削除イベント */
$(document).on("click", "#btn-delete", function(e) {
  let id = $("#delete-id").val();
  let url = DELETE_COMMENT_URL.replace("id", id);
  url = window.location.protocol + "//" + DOMAIN_INFO + url;
  console.log(url);
  window.location.href = url;

})

