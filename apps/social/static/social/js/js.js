function comment_form_display(post_id) {
    var x = document.getElementById('post-comment-' + post_id);
    var y = document.getElementById('post-caption-div-' + post_id);
    if (x.style.display === "none") {
        x.style.display = "flex";
    } else {
        x.style.display = "none";
    }

    if (y.style.display === "block") {
        y.style.display = "none";
    } else {
        y.style.display = "block";
    }
}

function comment_delete_display(comment_id){
    var x=document.getElementById('comment-delete-btn-'+comment_id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


function activity_display() {
    var activity= document.getElementById('activity-icon');

    var activities = document.getElementsByClassName('activities-a');

    if (activity.style.display === "block") {
        activity.style.display = "none";
    } else {
        activity.style.display = "block";
    }
        for (i=0; i<activities.length;i++ ){
            if (activities[i].style.display === "none") {
                activities[i].style.display = "flex";
            }
            else {
                activities[i].style.display = "none";
            }
        }
}

function show_comment_content(comment_id) {
    var x=document.getElementById('comment-content-'+comment_id);
        if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function show_followers() {
            var x = document.getElementById('follower-dpd-content');
            if (x.style.display === "none") {
                x.style.display = "flex";
            } else {
                x.style.display = "none";
            }

        }
function show_following() {
    var x = document.getElementById('following-dpd-content');
    if (x.style.display === "none") {
        x.style.display = "flex";
    } else {
        x.style.display = "none";
    }

}