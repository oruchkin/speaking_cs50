var down_vote_status = false
var up_vote_status = false

function like_function(question_id) {
    var like_button = document.getElementById('like-'+question_id);
    var dislike_button = document.getElementById('dislike-'+question_id);
    var counter_element = document.getElementById('counter-'+question_id);
    let current_counter = parseInt(counter_element.innerText);
    //console.log(current_counter)
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
        upvote_question_ajax(question_id, 2, 'upvote')
        dislike_button.className = 'vote_down_off'
        counter_element.innerText = current_counter
        like_button.className = 'vote_up_on'
    }
    // if like is not checked
    else {
        if (like_button.className == 'vote_up_off') {
            upvote_question_ajax(question_id, 1, 'upvote')
            if (up_vote_status == true){
            like_button.className = "vote_up_on"
            current_counter +=  1;
            counter_element.innerText = current_counter
            }

            //downvote and upvote (restricted animation)
            else {
                like_button.className = "vote_up_on"
                if (check_user == "AnonymousUser") {
                    show('You are not authorized','please log in')
                }
                else {
                    show('No! You can\'t upvote yourself!','This is illegal..')
                }
                setTimeout(() => {
                like_button.className = "vote_up_off"
                }, "250")
            }

        }
        else {
            upvote_question_ajax(question_id, -1, 'upvote')
            if (up_vote_status == true){
            like_button.className = "vote_up_off"
            current_counter +=  -1;
            counter_element.innerText = current_counter
            }
        }
    }
}



function dislike_function(question_id) {
    var like_button = document.getElementById('like-'+question_id);
    var dislike_button = document.getElementById('dislike-'+question_id);
    var counter_element = document.getElementById('counter-'+question_id);
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
        downvote_question_ajax(question_id, -2, 'downvote')
        like_button.className = 'vote_up_off'
        counter_element.innerText = current_counter
        dislike_button.className = "vote_down_on"
    }
    //if dis-like is not checked
    else {
        if (dislike_button.className == 'vote_down_off') {
            downvote_question_ajax(question_id, -1, 'downvote')
            if (down_vote_status == true){
                dislike_button.className = "vote_down_on"
                current_counter += -1;
                counter_element.innerText = current_counter
                down_vote_status = false
            }
            //downvote and upvote (restricted animation)
            else {
                dislike_button.className = "vote_down_on"
                if (check_user == "AnonymousUser") {
                    show('You are not authorized','please log in')
                }
                else {
                    show('No! You can\'t downvote yourself!','This is illegal..')
                }
                setTimeout(() => {
                dislike_button.className = "vote_down_off"
                }, "250")
            }
        }
        else {
            downvote_question_ajax(question_id, 1, 'downvote')
            if (down_vote_status == true){
                dislike_button.className = "vote_down_off"
                current_counter += 1;
                counter_element.innerText = current_counter
                down_vote_status = false
            }

        }
    }
}



function downvote_question_ajax(question_id, current_counter, vote_type) {
    var serialized_data = {
        'current_counter': current_counter,
        'question_id': question_id,
        'vote_type':vote_type
    }
    $.ajax({
        type: 'POST',
        url: "/ajax/question/downvote/",
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


function upvote_question_ajax(question_id, current_counter, vote_type) {
    var serialized_data = {
        'current_counter': current_counter,
        'question_id': question_id,
        'vote_type':vote_type
    }
    $.ajax({
        type: 'POST',
        url: "/ajax/question/upvote/",
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



