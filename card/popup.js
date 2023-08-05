
  document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const studentNumber = document.getElementById('student-number').value;
    const password = document.getElementById('password').value;
  
    chrome.tabs.create({ url: 'https://watcard.uwaterloo.ca/OneWeb/Account/LogOn', active: true }, function (tab) {
      // Wait for the login page to finish loading
          // Send login information to content script in the new tab
          chrome.tabs.sendMessage(tab.id, {type: "login", data: {studentNumber, password }});
        
      });
    });

  