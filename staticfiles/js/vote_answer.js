var down_vote_status = false
var up_vote_status = false

function like_function(answer_id) {
    var like_button = document.getElementById('like-'+answer_id);
    var dislike_button = document.getElementById('dislike-'+answer_id);
    var counter_element = document.getElementById('counter-'+answer_id);
    let current_counter = parseInt(counter_element.innerText);

    //check if like is on(true) or off(false)
    let dislike_state = false
    if (dislike_button.className == "vote_down_on") {
        dislike_state = true
    }
    else {
        dislike_state = false
    }
    //if like is checked
    if (dislike_state) {
        current_counter += 2;
        upvote_answer_ajax(answer_id, 2, 'upvote')
        dislike_button.className = 'vote_down_off'
        counter_element.innerText = current_counter
        like_button.className = 'vote_up_on'
    }
    // if like is not checked
    else {
        if (like_button.className == 'vote_up_off') {
            upvote_answer_ajax(answer_id, 1, 'upvote')
            if (up_vote_status == true){
            like_button.className = "vote_up_on"
            current_counter +=  1;
            counter_element.innerText = current_counter
            }

            //downvote and upvote (restricted animation)
            else {
                
                if (check_user == "AnonymousUser") {
                    show('You are not authorized','please log in')
                }
                else {
                    show('No! You can\'t upvote yourself!','This is illegal..')
                }
                like_button.className = "vote_up_on"
                setTimeout(() => {
                like_button.className = "vote_up_off"
                }, "250")
            }

        }
        else {
            upvote_answer_ajax(answer_id, -1, 'upvote')
            if (up_vote_status == true){
            like_button.className = "vote_up_off"
            current_counter +=  -1;
            counter_element.innerText = current_counter
            }
        }
    }
}


function dislike_function(answer_id) {
    var like_button = document.getElementById('like-'+answer_id);
    var dislike_button = document.getElementById('dislike-'+answer_id);
    var counter_element = document.getElementById('counter-'+answer_id);
    let current_counter = parseInt(counter_element.innerText);

    //check if like is on(true) or off(false)
    let like_state = false
    if (like_button.className == "vote_up_on") {
        like_state = true
    }
    else {
        like_state = false
    }
    //if dislike is checked
    if (like_state) {
        current_counter +=  -2;
        downvote_answer_ajax(answer_id, -2, 'downvote')
        like_button.className = 'vote_up_off'
        counter_element.innerText = current_counter
        dislike_button.className = "vote_down_on"
    }
    //if dis-like is not checked
    else {
        if (dislike_button.className == 'vote_down_off') {
            downvote_answer_ajax(answer_id, -1, 'downvote')
            if (down_vote_status == true){
                dislike_button.className = "vote_down_on"
                current_counter += -1;
                counter_element.innerText = current_counter
                down_vote_status = false
            }
            //downvote and upvote (restricted animation)
            else {
                if (check_user == "AnonymousUser") {
                    show('You are not authorized','please log in')
                }
                else {
                    show('No! You can\'t downvote yourself!','This is illegal..')
                }
                dislike_button.className = "vote_down_on"
                setTimeout(() => {
                dislike_button.className = "vote_down_off"
                }, "250")
            }
        }
        else {
            downvote_answer_ajax(answer_id, 1, 'downvote')
            if (down_vote_status == true){
                dislike_button.className = "vote_down_off"
                current_counter += 1;
                counter_element.innerText = current_counter
                down_vote_status = false
            }

        }
    }
}


function downvote_answer_ajax(answer_id, current_counter, vote_type) {
    var serialized_data = {
        'current_counter': current_counter,
        'answer_id': answer_id,
        'vote_type':vote_type
    }
    $.ajax({
        type: 'POST',
        url: "/ajax/answer/downvote/",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(serialized_data),
        async: false,
        success: function (event) {
            if (event['response_status'] == 'downvote_first_time' 
            || event['response_status'] == 'downvote_cancel'
            || event['response_status'] == 'downvote_from_upvote') {
                down_vote_status = true
            }
            else{
                down_vote_status = false
            }
        },
        error: function (event) {
            down_vote_status = false
        }
    });
}


function upvote_answer_ajax(answer_id, current_counter, vote_type) {
    var serialized_data = {
        'current_counter': current_counter,
        'answer_id': answer_id,
        'vote_type':vote_type
    }
    $.ajax({
        type: 'POST',
        url: "/ajax/answer/upvote/",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(serialized_data),
        async: false,
        success: function (event) {
            if (event['response_status'] == 'upvote_first_time' 
            || event['response_status'] == 'upvote_cancel'
            || event['response_status'] == 'upvote_from_downvote') {
                up_vote_status = true
            }
            else{
                up_vote_status = false
            }
        },
        error: function (event) {
            down_vote_status = false
        }
    });
}



// this is toggle share button ajax sender, question detailed page
function toggle_share_answer(answer_pk) {
    var answer_body = document.getElementById(answer_pk);
    let toggle_share_answer_id = 'share_togle_' + answer_pk
    let toggle_state = document.getElementById(toggle_share_answer_id).checked
    //сhanging body css
    if (toggle_state == true){
        answer_body.classList.remove("hide_share_answer");
        answer_body.classList.add("unhide_share_answer");
    }
    else {
        answer_body.classList.remove("unhide_share_answer");
        answer_body.classList.add("hide_share_answer");
    }
    var serialized_data = {
        'toggle_state': toggle_state,
        'toggle_share_answer_id': answer_pk,
    }
    $.ajax({
        type: 'POST',
        url: "/ajax/share_answer/",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(serialized_data),
        async: false,
    });
}
