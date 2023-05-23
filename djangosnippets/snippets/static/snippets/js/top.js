"use strict";

// スニペット削除URL
var DELETE_SNIPPET_URL = "/snippets/id/delete/";

/** テーブル背景色 */
$(".th-color").css("background-color", "#f8f8f8");

/** オンロードイベント */
$(function () {
  $(".snippet_category").each((i, e) => {
    // スニペットのカテゴリ名セット
    let val = $(e).text();
    $(e).text(CATEGORYS[val]);

    // セレクトボックスの初期値セット
    let key = $("#search_category").attr("data-value");
    $("select[id=search_category] option").each((i, e) => {
      let $e = $(e);
      if (key === $e.val()) {
        $e.prop("selected", true);
      }
    });
  });
});

/** スニペット削除モーダル表示イベント */
$(document).on("click", ".btn-delete", function(e) {
  // モーダル情報セット
  let sId = $(e.target.closest(".delete-content")).find("input[name=itemId]").val();
  $("#delete-id").val(sId);
  let sName = $(e.target.closest(".delete-content")).find("input[name=itemName]").val();
  $("#delete-title").text(sName);

  // モーダル表示
  var myModal = new bootstrap.Modal($("#myModal"));
  myModal.show();
});

/** モーダル閉じるイベント */
$(document).on("click", ".modal-close", function(e) {
  $(".modal-backdrop").hide();
});

/** スニペット削除イベント */
$(document).on("click", "#btn-delete", function(e) {
  let id = $("#delete-id").val();
  let url = DELETE_SNIPPET_URL.replace("id", id);
  url = window.location.protocol + "//" + DOMAIN_INFO + url;
  window.location.href = url;
})