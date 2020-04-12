
window.onload = function() {
	
	document.querySelector('#send').onclick = function() {
		alert('Hello')
		var inp_comment_text = document.querySelector('textarea[name = text]');
		var inp_author_engraver = document.querySelector('input[name = author_engraver]');
		var inp_recipient_engraver = document.querySelector('input[name = recipient_engraver]');
		var params = 'text=' + inp_comment_text.value + '&' + 'recipient_engraver=' + inp_recipient_engraver.value + '&' + 'author_engraver=' + inp_author_engraver.value;
		ajaxPostCommenEngraverProfile(params);
	}
	function ajaxPostCommenEngraverProfile(params) {
		$.ajax({
			type: "POST",
			url: "/add_comment",
			data: params,
			success: function(html) {
				
			}
		});
		return false;
	};


	document.querySelector('#del_comment_profile_engraver').onclick = function() {
		var value_comment_id_profile_engraver = document.querySelector('input[name = comment_id]')
		var value_comment_user_profile_engraver = document.querySelector('input[name = comment_user]')
		var  comment = 'comment_id=' + value_comment_id_profile_engraver.value + '&' + 'comment_user=' + value_comment_user_profile_engraver.value;
		ajaxDeleteCommentProfileEngraver(comment);
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
	
	}
}

document.querySelector('#topic_event_like_up_photo').onclick = function() {
	var inp_event_id = document.querySelector('input[ name = event_id ');
	var inp_photo_id = document.querySelector('input[ name = photo_id ');
	var inp_like_way = document.querySelector('input[ name = way_like_up');
	var inp_like_up = document.querySelector('input[ name = like_up');
	var params_like_up = 'event_id=' + inp_event_id.value + '&' + 'photo_id=' + inp_photo_id.value + '&' + 'way_like_up=' + inp_like_way.value + '&' + 'like_up=' + inp_like_up.value;
	ajaxLikeUpPhotoTopicEvent(params_like_up);
}

function ajaxLikeUpPhotoTopicEvent(params_like_up) {
	$.ajax({
		type: "POST",
		url: "/add_like_up_to_photo_event",
		data: params_like_up,
		success: function(html) {
			location.reload()
		}
	});
	return false;
};

document.querySelector('#topic_event_like_down_photo').onclick = function() {
	var inp_event_id = document.querySelector('input[ name = event_id ');
	var inp_photo_id = document.querySelector('input[ name = photo_id ');
	var inp_like_way = document.querySelector('input[ name = way_like_down');
	var inp_like_down = document.querySelector('input[ name = like_down');
	var params_like_down = 'event_id=' + inp_event_id.value + '&' + 'photo_id=' + inp_photo_id.value + '&' + 'way_like_down=' + inp_like_way.value + '&' + 'like_down=' + inp_like_down.value;
	ajaxLikeDownPhotoTopicEvent(params_like_down);
}

function ajaxLikeDownPhotoTopicEvent(params_like_down) {
	$.ajax({
		type: "POST",
		url: "/add_like_down_to_photo_event",
		data: params_like_down,
		success: function(html) {
			location.reload()
		}
	});
	return false;
};