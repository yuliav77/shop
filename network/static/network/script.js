document.addEventListener('DOMContentLoaded', function() {

/* Show all posts */
	load_posts();

	var authenticated_user = document.querySelector('#username');
	if (authenticated_user){ 
	/* Add new post */	
		document.querySelector('#add_post').style.dispay = "block";
		document.querySelector('#add_post').onsubmit = () => {
		
			const post_text = document.querySelector('#post-text').value;
			
			fetch('/posts', {
				method: 'POST',
				body: JSON.stringify({
					post_text: post_text
				})
			})
			.then(response => response.json())
			.then(result => {
				console.log(message);
			});
		}
		
		/* Load FOLLOWING posts*/	
		document.querySelector('#following_link').onclick = () => {
			
			document.querySelector('#user_info').innerHTML = "";
			load_posts("following");
			return false
		}
	}	
	else {
		document.querySelector('#add_post').style.display = "none";
	}
	
	

			

});


/* Load user info */
function load_user(username) {

	var user_info = document.querySelector('#user_info');
	var current_user = document.querySelector('#username').innerText;
	user_info.innerHTML = "";
	
		fetch('/users/' + username)
		.then(response => response.json())
		.then(user => {
			const user_followers = user.followers.length;			
			const user_following = user.following.length;	
			let span_followers = document.createElement('span');
			let span_following = document.createElement('span');
			span_followers.setAttribute("class","follow_span");
			span_followers.setAttribute("id","followers_span");
			span_following.setAttribute("class","follow_span");
			span_following.setAttribute("id","following_span");
			span_followers.append(user_followers);
			span_following.append(user_following);
			user_info.append("Followers: ", span_followers);
			user_info.append("Following: ", span_following);
			
			if (current_user != username){
				var follow_flag = false;
				let follow_button = document.createElement('button');
				follow_button.setAttribute("class","follow_button");
				for (let i = 0; i < user.followers.length; i++){
					if (user.followers[i] == current_user){
						follow_button.append("UNFOLLOW");
						follow_flag = true;
						break
					}
				}
				if ( !follow_flag )
					follow_button.append("FOLLOW");
				
				user_info.append(follow_button);
				
				document.querySelector('.follow_button').onclick = function(e) {
					change_follow(current_user, username, follow_flag);
					follow_flag = !follow_flag;
					if (follow_flag){
						e.currentTarget.innerText = "UNFOLLOW";
						let followers_counter = document.querySelector('#followers_span').innerText;
						document.querySelector('#followers_span').innerText = Number(followers_counter) + 1;
					}	
					else {
						let followers_counter = document.querySelector('#followers_span').innerText;
						document.querySelector('#followers_span').innerText = Number(followers_counter) - 1;
						e.currentTarget.innerText = "FOLLOW";
					}	
						
				}
				
			}
		});
	
	
}

/* Follow/UnFollow  function */
function change_follow(who_follow, whom_follow, follow_flag){
	
	fetch('/users/' + whom_follow, {
		method: 'PUT',
		body: JSON.stringify({
			who_follow: who_follow,
			follow_flag: follow_flag
		})
	})
	

}

/* load posts function */
function load_posts(username,page) {
	
	var posts_block = document.querySelector('#posts_view');
	posts_block.innerHTML = "";
	var current_user_block = document.querySelector('#username');
	if (current_user_block) 
		var current_user = current_user_block.innerText;
	else 
		var current_user = "";


	if (username){
		if ( username != "following" && username != "None"){ 
			/* load USER posts */
			if (page)
				var path = '/posts/' + username + '?page=' + page;
			else	
				var path = '/posts/' + username;
			document.querySelector('h1').innerText = username;
			document.querySelector('h1').setAttribute('id','username_title');
			document.querySelector('#add_post').style.display = 'none';
		}
		else if ( username === "following" ){
			/* load FOLLOWING posts */
			var path = '/following';
			document.querySelector('h1').innerText = "Following";
			document.querySelector('#add_post').style.display = 'none';			
		}
		else if (username === "None") {
			/* Load ALL posts (some page) */
			var path = '/posts?page=' + page;
		}
	}
	else {
		var path = '/posts';
	}
		
		fetch(path)
		.then(response => response.json())
		.then(posts => {
				// Print posts
				if (posts.data.length == 0)
					posts_block.append("No posts here yet!");
				else {	
				
				
					// Pagination
				
					if (posts.previous_page || posts.next_page){
						let pagination = document.createElement('nav');
						let pagination_ul = document.createElement('ul');
						pagination_ul.setAttribute("class","pagination");
						let pagination_ul_li_prev = document.createElement('li');
						pagination_ul_li_prev.setAttribute("class","page-item");
						let pagination_ul_li_next = document.createElement('li');
						pagination_ul_li_next.setAttribute("class","page-item");
						
						if (!posts.previous_page) {
							pagination_ul_li_prev.classList.add("disabled");
						}
						let pagination_ul_li_prev_a = document.createElement('a');
						pagination_ul_li_prev_a.setAttribute("class","page-link");
						pagination_ul_li_prev_a.append("Previous");
						pagination_ul_li_prev.append(pagination_ul_li_prev_a);
						pagination_ul.append(pagination_ul_li_prev);

						for (let k = 0; k < posts.num_pages; k++){
							let pagination_ul_li = document.createElement('li');
							pagination_ul_li.setAttribute("class","page-item");
							let page_k = k + 1;
							
							if ( page_k === posts.number){
								pagination_ul_li.classList.add("active");
							}	
							
							let pagination_ul_li_a = document.createElement('a');
							pagination_ul_li_a.setAttribute("class","page-link");
							pagination_ul_li_a.append(k + 1);
							pagination_ul_li.append(pagination_ul_li_a);
							pagination_ul.append(pagination_ul_li);
						}
						
						if (!posts.next_page) {
							pagination_ul_li_next.classList.add("disabled");
						}
						let pagination_ul_li_next_a = document.createElement('a');
						pagination_ul_li_next_a.setAttribute("class","page-link");
						pagination_ul_li_next_a.append("Next");
						pagination_ul_li_next.append(pagination_ul_li_next_a);
						pagination_ul.append(pagination_ul_li_next);

						
						
						pagination.append(pagination_ul);
						posts_block.append(pagination);
						
						let page_links = document.querySelectorAll('.page-link');
						[].forEach.call(page_links, function(el) {
							el.onclick = function(e) {
								
								let a_text = e.currentTarget.innerText;
								if (a_text == "Previous")
									page = posts.previous_page;
								else if (a_text == "Next")
									page = posts.next_page;
								else 
									page = a_text;
								var username_title = document.querySelector('#username_title');
								if (username_title) {
										load_posts(username_title.innerText, page)
									}
								else{	
									load_posts("None", page)
								}
								return false
							}
						});

					}

				
				//Posts 
				
					for (let i = 0; i < posts.data.length; i++) {
						let post_div = document.createElement('div');
						post_div.setAttribute("class","post_div");
						const post_id = posts.data[i].id;
						const post_author = posts.data[i].author;
						const post_text = posts.data[i].text;
						const post_date = posts.data[i].timestamp;
						const post_counter = posts.data[i].counter;
						let author = document.createElement('h3');
						let author_a = document.createElement('a');
						author_a.innerText = post_author;
						author_a.title = post_author;
						author_a.setAttribute("class","username");
						author.append(author_a);
						
						post_div.append(author);
						
						if (post_author === current_user){
							let edit_button = document.createElement('button');
							edit_button.append("Edit post");
							
							edit_button.onclick = function(e) {
							
								var post_text_div = e.currentTarget.nextElementSibling;
								post_text_div.innerHTML = "";
								
								let edit_text_form = document.createElement('form');
								edit_text_form.setAttribute("class","edit_text_form");
								
								let post_textarea = document.createElement('textarea');
								post_textarea.innerText = post_text;
								edit_text_form.append(post_textarea);
								
								let edit_form_save_button = document.createElement('button');
								let edit_form_cancel_button = document.createElement('button');
								edit_form_save_button.append("Save");
								edit_form_cancel_button.append("Cancel");
								
									edit_form_save_button.onclick = function(e) {
										let edited_text = e.currentTarget.previousElementSibling.value;
										edit_post(post_id, edited_text);
										post_text_div.innerHTML = "";
										post_text_div.append(edited_text);
										return false
									}
									
									edit_form_cancel_button.onclick = function(e) {
										post_text_div.innerHTML = "";
										post_text_div.append(post_text);
										return false
									}
								
								edit_text_form.append(edit_form_save_button);
								edit_text_form.append(edit_form_cancel_button);
								post_text_div.append(edit_text_form);
								
								
								return false
							}
							
							post_div.append(edit_button);
							
							
						}
						
						let post_text_div = document.createElement('div');
						post_text_div.setAttribute("class","post_text_div");
						post_text_div.append(post_text);
						post_div.append(post_text_div);
						
						let timestamp = document.createElement('div');
						timestamp.setAttribute("class","timestamp_div");
						timestamp.append(post_date);
						post_div.append(timestamp);
						let counter_block = document.createElement('div');
						let counter_button = document.createElement('button');
						let counter_text = document.createElement('span');
						counter_button.setAttribute("class","counter_button");
						counter_button.setAttribute("data-id", posts.data[i].id);
						if (post_counter > 0) 
							counter_button.style.color = "red"
						
						counter_text.append(post_counter);
						counter_block.append(counter_button,counter_text);
						post_div.append(counter_block);
						
						posts_block.append(post_div);
					}
					
						var authenticated_user = document.querySelector('#username');
						if (authenticated_user){
							let like_buttons = document.querySelectorAll('.counter_button');
							[].forEach.call(like_buttons, function(el) {
								el.onclick = function(e) {
								
									change_liked(e.currentTarget.dataset.id);
									return false
								
								}
							});
							
							let users_names = document.querySelectorAll('.username');
							[].forEach.call(users_names, function(el) {
								el.onclick = function(e) {
									let username = e.currentTarget.innerText;
									load_user(username);
									load_posts(username);
									return false
								}
							});
						}

				
						
				}

		});		
}


function change_liked(post_id){

	fetch('/posts/' + post_id)
	.then(response => response.json())
	.then(post => {
		document.querySelector("[data-id='" + post_id + "']").nextElementSibling.textContent = post.counter;
		if (post.counter > 0)
			document.querySelector("[data-id='" + post_id + "']").style.color = "red"
		else
			document.querySelector("[data-id='" + post_id + "']").style.color = "black"
			
	});
	
	
}


function edit_post(post_id, edited_text){

	fetch('/posts/' + post_id, {
		method: 'PUT',
		body: JSON.stringify({
			post_id: post_id,
			post_text: edited_text
		})
	})
	
}
