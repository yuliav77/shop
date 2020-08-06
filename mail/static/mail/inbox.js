document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());


  
  // By default, load the inbox
	load_mailbox('inbox');
  
	document.querySelector('#compose-form').onsubmit = () => {
		const recipients = document.querySelector('#compose-recipients').value;
		const subject = document.querySelector('#compose-subject').value;
		const body = document.querySelector('#compose-body').value;
		fetch('/emails', {
			method: 'POST',
			body: JSON.stringify({
				recipients: recipients,
				subject: subject,
				body: body
			})
		})
		.then(response => response.json())
		.then(result => {
			// Print result
			console.log(result);
			console.log('recipients:', recipients, "subject:", subject, "body:", body);
			load_mailbox('sent');
		});
  		return false;
	}
	
	
	
});

function compose_email(recipients, subject, body, timestamp) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out or fill composition fields
		if (recipients == null) {
			document.querySelector('#compose-recipients').value = ''; 
		}
		else {
			document.querySelector('#compose-recipients').value = recipients;
		}	
		
		if (subject == null) {
			document.querySelector('#compose-subject').value = ''; 
		}	
		else {
			let number = subject.indexOf('Re:');
			console.log(number);
			if ((number == -1) || (number > 1))
				document.querySelector('#compose-subject').value = "Re: " + subject;
			else document.querySelector('#compose-subject').value = subject;
		}
		
		if (body == null) document.querySelector('#compose-body').value = ''; 
		else document.querySelector('#compose-body').value = "\nOn " + timestamp + " " + recipients + " wrote:\n\n" + body;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
	fetch('/emails/' + mailbox)
	.then(response => response.json())
	.then(emails => {
			// Print emails
			console.log(emails);
			console.log("Mailbox:" + mailbox + "!");
			if (emails.length == 0)
				document.querySelector('#emails-view').append("No emails here yet!");
			else {	
				table = document.createElement('table');
				table.setAttribute("id","emails-table");
				document.querySelector('#emails-view').append(table);
				document.querySelector('#emails-table').innerHTML = "";
				const th = document.createElement('tr');
				var th_text = "<tr><th>";
				if (mailbox == "sent") 
					th_text += "Recipients";
				else 
					th_text += "Sender";
				th_text += "</th><th>Subject</th><th>Timestamp</th></tr>"
				th.innerHTML = th_text;
				document.querySelector('#emails-table').append(th);
				for (let i = 0; i < emails.length; i++) {
					let tr = document.createElement('tr');
					tr.setAttribute("data-id",emails[i].id);
					if (emails[i].read) 
						tr.style.background = "#c5c5c5"
					else 
						tr.style.background = "white"				
					var tr_text = "<td>";
					if (mailbox == "sent") 
						tr_text += emails[i].recipients;
					else 	
						tr_text += emails[i].sender;
					tr_text += "</td><td>" + emails[i].subject + "</td><td>" + emails[i].timestamp + "</td>"
					tr.innerHTML = tr_text; 
					document.querySelector('#emails-table').append(tr);
				}
				
				let letters_tr = document.querySelectorAll('table#emails-table > tr');
				[].forEach.call( letters_tr, function(el) {
					el.onclick = function(e) {
						show_letter(e.currentTarget.dataset.id, mailbox);
						return false;
					}
				});
			}
	});
	

}

function show_letter(letter_id, letter_mailbox){
		document.querySelector('#emails-view').style.display = 'none';
		document.querySelector('#email-view').style.display = 'block';
		document.querySelector('#compose-view').style.display = 'none';
		
  					document.querySelector('#archive_button').addEventListener('click', () => {
						mark_status(letter_id, 'archived');
						load_mailbox('inbox')
					});					
					document.querySelector('#unarchive_button').addEventListener('click', () => {
						mark_status(letter_id, 'unarchived');
						load_mailbox('inbox')
					});


		fetch('/emails/' + letter_id)
			.then(response => response.json())
			.then(email => {
				// Print email
				console.log(email);
				document.querySelector('#sender span').innerHTML = email.sender;
				document.querySelector('#recipients span').innerHTML = email.recipients;
				document.querySelector('#subject span').innerHTML = email.subject;
				document.querySelector('#timestamp span').innerHTML = email.timestamp;
				document.querySelector('#body textarea').innerHTML = email.body;
				const sender = email.sender;
				if (letter_mailbox == "inbox") {
					document.querySelector('#archive_button').style.display = 'block';
					document.querySelector('#reply_button').style.display = 'block';
					document.querySelector('#unarchive_button').style.display = 'none';
					document.querySelector('#reply_button').addEventListener('click', () => compose_email(email.sender, email.subject, email.body, email.timestamp));
				}
				else if (letter_mailbox == "archive"){
					document.querySelector('#unarchive_button').style.display = 'block';
					document.querySelector('#reply_button').style.display = 'none';
					document.querySelector('#archive_button').style.display = 'none';
				}
				else if (letter_mailbox == "sent"){
					document.querySelector('#unarchive_button').style.display = 'none';
					document.querySelector('#archive_button').style.display = 'none';
					document.querySelector('#reply_button').style.display = 'none';
				}
				if (!email.read) 
					mark_status(letter_id, "read");
		});
}

function mark_status(letter_id, letter_status){
		if (letter_status == "read") {
			fetch('/emails/' + letter_id, {
				method: 'PUT',
				body: JSON.stringify({
					read: true
				})
			})
		}	
		else if (letter_status == "archived") {
			fetch('/emails/' + letter_id, {
				method: 'PUT',
				body: JSON.stringify({
					archived: true
				})
			})
		}	
		else if (letter_status == "unarchived") {
			fetch('/emails/' + letter_id, {
				method: 'PUT',
				body: JSON.stringify({
					archived: false
				})
			})
		}	
}