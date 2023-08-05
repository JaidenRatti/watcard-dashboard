// contentScript.js

// Listen for messages from the popup script
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.type === "login") {
      const { studentNumber, password } = message.data;
      const result = loginToWebsite(studentNumber, password);
    }
  });
  
  function loginToWebsite(studentNumber, password) {
    // Wait for the website to load before filling in the login form
      // Fill in the login form with the provided studentNumber and password
      document.getElementById('Account').value = studentNumber;
      document.getElementById('Password').value = password;  
      // Submit the login form
      document.getElementsByClassName('btn ow-btn-primary btn-block-xs pull-right').click();
      const testing = document.getElementById('account-id');
      return testing !== null;
  }
  