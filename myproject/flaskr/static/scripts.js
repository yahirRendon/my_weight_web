var userId = null;          // store userid

/**
 * Run function with window loads to check which page the user is on
 * and populate data as needed
 */
window.onload = function() {
    var indexPage = document.getElementById('index_page');
    var indexUserPage = document.getElementById('index_user_page');

    getUser();

    if(indexPage) {
        displayPosts();
    } else
    if(indexUserPage) {
        displayUserPosts();
    } 
}

/**
 * request and update the userId
 */
function getUser() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'http://127.0.0.1:5000/getuser', false ); // false for synchronous request
    // xmlHttp.open( "GET", 'http://127.0.0.1:5000/test/2/posts', false ); // false for synchronous request
    xmlHttp.send( null );
    
    userId = parseInt(xmlHttp.responseText);
}

/**
 * Display all the posts in the database
 */
function displayPosts() {
    // get the data
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'http://127.0.0.1:5000/posts', false ); // false for synchronous request
    // xmlHttp.open( "GET", 'http://127.0.0.1:5000/test/2/posts', false ); // false for synchronous request
    xmlHttp.send( null );
    
    var data = JSON.parse(xmlHttp.responseText);

    // build the post display
    buildPostHTML(data);
}

/**
 * Display all of the logged in user's post
 */
function displayUserPosts() {
    // get the data
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'http://127.0.0.1:5000/user/'+userId+'/posts', false ); // false for synchronous request
    // xmlHttp.open( "GET", 'http://127.0.0.1:5000/test/2/posts', false ); // false for synchronous request
    xmlHttp.send( null );
    
    var data = JSON.parse(xmlHttp.responseText);

    // build the post display
    buildUserPostHTML(data);
}

/**
 * build the html and populate with json data
 * 
 * @param {json array}      data 
 */
function buildPostHTML(data) {
    // get the parent element from html
    var wrap = document.getElementsByClassName('post')[0];

    // loop through the data and build posts layout
    for(var i = 0; i < data.length; i++) {

        // console.log(data[i].author_id);
        var elem = null;
        if(data[i].author_id == userId) {
        
        elem = 
        `
        <div class="wrap_post_out">
        <div class="wrap_post">
        <div class="e_post p_a">${data[i].created}</div>
        <div class="e_post p_b">${data[i].weight}</div>
        <div class="e_post p_c">${data[i].body}</div>
        <div class="e_post p_d">${data[i].username}</div>
        <div class="e_post p_e">
            <a href="http://127.0.0.1:5000//${data[i].id}/update">Edit</a>
        </div>
        </div>
        </div>
        `
        } else {
            elem = 
        `
        <div class="wrap_post_out">
        <div class="wrap_post">
        <div class="e_post p_a">${data[i].created}</div>
        <div class="e_post p_b">${data[i].weight}</div>
        <div class="e_post p_c">${data[i].body}</div>
        <div class="e_post p_d">${data[i].username}</div>
        <div class="e_post p_e">
            <a href="http://127.0.0.1:5000//${data[i].id}/update"></a>
        </div>
        </div>
        </div>
        `
        }
        wrap.innerHTML += elem;        
    }
}

/**
 * build the html and populate with json data
 * 
 * @param {json array}      data 
 */
 function buildUserPostHTML(data) {
    if(data.length > 0 ) {
        var currentWeight = data[0].weight;
        var targetWeight = data[0].goalweight;
        var weightDiff = parseInt(currentWeight) - parseInt(targetWeight);
        var toGoalStr = "+";
        if(weightDiff < 0) {
            toGoalStr = "-";
        }
     
        document.getElementsByClassName("circle")[0].innerHTML = currentWeight + " lbs";
        document.getElementsByClassName("circle")[1].innerHTML = toGoalStr + Math.abs(weightDiff).toString(); 
        document.getElementsByClassName("circle")[2].innerHTML = targetWeight + " lbs";

        // get the parent element from html
        var wrap = document.getElementsByClassName('post')[0];

        // loop through the data and build posts layout
        for(var i = 0; i < data.length; i++) {
            currentWeight = data[i].weight;
            var elem = null;
            
            elem = 
            `
            <div class="wrap_post_out">
            <div class="wrap_post">
            <div class="e_post p_a">${data[i].created}</div>
            <div class="e_post p_b">${data[i].weight}</div>
            <div class="e_post p_c">${data[i].body}</div>
            <div class="e_post p_d">${data[i].username}</div>
            <div class="e_post p_e">
                <a href="http://127.0.0.1:5000//${data[i].id}/update">Edit</a>
            </div>
            </div>
            </div>
            `     
            wrap.innerHTML += elem;       
        }
    }  
}

