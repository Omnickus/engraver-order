
window.onload = function() {
	
	document.querySelector('#send').onclick = function() {
		var inp_comment_text = document.querySelector('textarea[name = text]');
		var inp_author_engraver = document.querySelector('input[name = author_engraver]');
		var inp_recipient_engraver = document.querySelector('input[name = recipient_engraver]');
		var params = 'text=' + inp_comment_text.value + '&' + 'recipient_engraver=' + inp_recipient_engraver.value + '&' + 'author_engraver=' + inp_author_engraver.value
		ajaxPost(params, inp_recipient_engraver);
	}
	function ajaxPost(params, inp_recipient_engraver) {
		$.ajax({
			type: "POST",
			url: "/add_comment",
			data: params,
			success: function(html) {
				location.reload()
			}
		});
		return false;
	};
	document.querySelector('#del_comment_profile_engraver').onclick = function() {
		var value_comment_id_profile_engraver = document.querySelector('input[name = comment_id]')
		var value_comment_user_profile_engraver = document.querySelector('input[name = comment_user]')
		var  comment = 'comment_id=' + value_comment_id_profile_engraver.value + '&' + 'comment_user=' + value_comment_user_profile_engraver.value
		ajaxDeleteCommentProfileEngraver(comment);
	}
}


function ajaxDeleteCommentProfileEngraver(comment) {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if(request.readyState == 4 && request.status == 200) {
			document.querySelector('#result').innerHTML = request.responseText;
			location.reload()
		}
	}
	request.open('POST', '/delete-comment/');
	request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
	request.send(comment);
}
