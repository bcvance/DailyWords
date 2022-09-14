const exitBtnHTML = `
<div class="close-time-input">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
    </svg>
</div>
`

// show input field for phone number when send to phone box is checked
const phoneInput = document.getElementById('phone');
phoneInput.onclick = () => {
    if (document.getElementById('phone').checked) {
        document.getElementById('numberfield').style.display = 'block';
    }
    else {
        document.getElementById('numberfield').style.display = 'none';
    }
}

// append time field on click of "add another time"
document.getElementById('add-time').onclick = () => {
    // get and clone existing time field
    const timeField = document.getElementsByClassName('time-field')[0];
    const newElement = timeField.cloneNode(true);
    // for all additional time fields, add a close button to delete the field if needed
    let exitBtn = document.createElement('template');
    exitBtn.innerHTML = exitBtnHTML.trim()
    exitBtn = exitBtn.content.firstElementChild;
    newElement.appendChild(exitBtn);
    // add event listener to close button for each added input field
    newElement.childNodes[5].onclick = (event) => {
        newElement.remove()
    }
    // add new input field to bottom of "time-component" div
    const parentNode = document.getElementById('time-component');
    parentNode.appendChild(newElement);
}

// save updated user options to database
function saveOptions() {
    let hours = document.getElementsByClassName('time');
    let amPms = document.getElementsByClassName('am-pm');
    let timeVals = [];
    let hour;
    let amPm;
    for (let i=0; i<hours.length; i++) {
        hour = hours[i].value;
        amPm = amPms[i].value;
        if (hour !== '12') {
            if (amPm === 'pm') {
                hour = (Number(hour) + 12)
            }
            else {
                hour = Number(hour);
            }
        }
        else {
            if (amPm === 'am') {
                hour = 0;
            }
        }

        // adjust time input to UTC
        const localDateTime = new Date();
        const timeZoneOffset = Math.floor(localDateTime.getTimezoneOffset() / 60);
        hour -= timeZoneOffset
        if (hour < 0) {
            hour += 24;
        }
        else if (hour > 23) {
            hour -= 24
        }
        timeVals.push(hour);
    }
    console.log(timeVals);
    chrome.storage.sync.set({
        sendToPhone: phoneInput.checked,
        sendToEmail: document.getElementById('email').checked,
        phoneNumber: document.getElementById('number').value,
        numWords: document.getElementById('num-words').value,
        timeVals: timeVals
    }, function() {
        // tell background.js to save new settings to database (can't make API call from options.js due to CORS)
        chrome.runtime.sendMessage({type: 'saveOptions'})
        // update status to let user know options were saved
        let status = document.getElementById('status');
        status.textContent = 'Preferences Saved.';
        setTimeout(function() {
            status.textContent = '';
        }, 1000);
    }); 
}

function restoreOptions() {
    chrome.storage.sync.get({
        sendToPhone: false,
        sendToEmail: false,
        phoneNumber: '',
        numWords: 5
    }, function(items) {
        phoneInput.checked = items.sendToPhone;
        document.getElementById('email').checked = items.sendToEmail;
        document.getElementById('num-words').value = items.numWords;
        if (phoneInput.checked) {
            document.getElementById('numberfield').style.display = 'block';
        }
        document.getElementById('number').value = items.phoneNumber;
    })
}

document.addEventListener('DOMContentLoaded', restoreOptions);

// save settings
document.getElementById('save').addEventListener('click', function() {
    
    // in case user has not been authenticated by activate extension on a page,
    // we will authenticate and fetch their user info now
    chrome.runtime.sendMessage({type: 'authorize', origin: 'options'});  
});

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.type === 'auth_completed') {
            saveOptions();
        }
    }
)

// function to create html element from html string
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}