const base_url = "localhost:5000";
const INITIAL_PRESET = 1;
const sample_pdf_uri = "sample_pdf.html";
const blank_uri = "blank.html";

const BLANK = Symbol("BLANK");
const PDF = Symbol("PDF");
const SPOTIFY = Symbol("SPOTIFY");

var presets = {
    1: [[BLANK]],
    2: [[BLANK], [BLANK]],
    3: [[BLANK, BLANK], [BLANK]]
}
var preset = INITIAL_PRESET;

function bodyOnload() {
    var webpage = window.location.href;
    console.log("Page Loaded: " + webpage);
    if (webpage.indexOf('chungus') !== -1) {
        chungusInit();
    }
    else if (webpage.indexOf('smol') !== -1) {
        smolInit();
    }
}

// This was necessary for Chungus scrolling to work correctly. Figure out how to not use this!!
// function iframeOnload() {
//     bodyOnload();
// }


function chungusInit() {
    console.log("Page Init: Chungus");
    var socket = io.connect(base_url);
    const urlParams = new URLSearchParams(window.location.search);
    const session_id = urlParams.get('desk_token');
    if (session_id === undefined) {
        console.log("Chungus: SESSION ID NOT FOUND")
    }

    socket.on('connect', function() {
        socket.emit("chungus-ready", session_id);
    });

    socket.on("chungus-init", function(elem) {
        var page = document.getElementById("display-page");
        page.innerHTML = elem;

        socket.on("chungus-template-response", function(msg) {
            insertContent(msg['content'], msg['type'], msg['col'], msg['row']);
        });

        // Listener for pdf scroll from Flask App
        socket.on('pdf-scroll-event', function(msg) {
            // console.log(msg);
            if (msg[0] === 'Down') {
                pdfScroll(msg[1], 0)
            }
            else if (msg[0] === 'Up') {
                pdfScroll(msg[1], 1)
            }
        });

        // According to preset, fill in divs
        fillPresetDivs(session_id, socket, presets[preset]);

        // Create psuedo-grid on smol to match chungus's display
        socket.emit('smol-create-panel', session_id, preset, presets);
    });

    socket.on('change-preset', function(msg) {
        let p = msg['p'];
        let elem = msg['elem'];
        console.log("Changing preset to " + p);
        preset = p;
        let page = document.getElementById("display-page");
        page.innerHTML = elem;
        fillPresetDivs(session_id, socket, presets[preset]);

        // Create psuedo-grid on smol to match chungus's display
        socket.emit('smol-create-panel', session_id, preset, presets);
    });

    socket.on('chungus-handle-pdf', function(data) {
        let c = data['col'];
        let r = data['row'];
        let fileURL = data['fileURL'];

        let id = `pdf-iframe-c${c}r${r}`;
        console.log(id);

        let frame = document.getElementById(id);
        frame.src = fileURL;
    });

}

https://stackoverflow.com/questions/9643311/pass-a-string-parameter-in-an-onclick-function
function smolInit() {
    console.log("Page Init: smol");
    const urlParams = new URLSearchParams(window.location.search);
    const session_id = urlParams.get('desk_token');
    if (session_id === undefined) {
        console.log("smol: SESSION ID NOT FOUND")
    }

    var socket = io.connect(base_url);
    socket.on('connect', function() {
        socket.emit("smol-ready", session_id);
    });

    socket.on('smol-init', function() {
        for (let p = 1; p < Object.keys(presets).length + 1; p++) {
            let id = `preset-${p}`;
            let button = document.createElement('input');
            button.type = "button"
            button.id = id;
            button.value = id;
            button.addEventListener('click', function(){
                requestChangePreset(socket, session_id, p);
            });
            document.getElementById('preset-buttons-div').appendChild(button);
        }
    });

    socket.on('create-smol-panel', function(data) {
        let panelDiv = document.getElementById('ctrl-panel');
        panelDiv.textContent = '';
        let rows = data['rows'];
        let template = data['template'];

        for (let c = 0; c < rows.length; c++) {
            let newCol = document.createElement('div');
            newCol.classList.add('col');
            newCol.id = `ctrl-panel-c${c+1}`;
            
            for (let r = 0; r < rows[c]; r++) {
                let newRow = document.createElement('div');
                newRow.id = `ctrl-panel-c${c+1}r${r+1}`
                newRow.classList.add('row');
                newRow.style.textAlign = 'center';
                newRow.classList.add('show-border');
                newRow.classList.add(`rows-${rows[c]}`);
                newRow.innerHTML = template;
                newCol.appendChild(newRow);

                // Upload button
                let uploadButton = document.createElement('input');
                uploadButton.type = 'button';
                uploadButton.value = 'Upload';
                uploadButton.addEventListener('click', function(){
                    nosePicker(socket, session_id, c+1, r+1);
                });
                newCol.appendChild(uploadButton);

            }
            panelDiv.appendChild(newCol);
        }

        let buttons = document.getElementsByClassName('choice');
        for (let i = 0; i < buttons.length; i++) {
            const button = buttons[i];
            button.addEventListener('click', function(){
                    console.log(button.id);
                    socket.emit('smol-request-template', session_id, button.parentNode.id, button.value);
            });
        }
    });
}


function pdfScroll(col_row, dir) {
    let frame_name = `pdf-iframe-${col_row}`;
    let div_name = `pdf-div-${col_row}`;
    var iframe = document.getElementById(frame_name);
    var iframeDiv = document.getElementById(div_name);
    if (iframeDiv === null || iframe === null) return;

    console.log("Attempting to scroll " + col_row);
    
    var scrollTarget = iframeDiv.scrollTop;
    (dir ? scrollTarget -= 30 : scrollTarget += 30);
    if (scrollTarget < 0) scrollTarget = 0;
    iframeDiv.scrollTo({
        top: scrollTarget,
        // behavior: 'smooth'
    });

    // If we didn't scroll enough (hit bottom of div), increase height and scroll again
    if (iframeDiv.scrollTop < (scrollTarget) && !dir) {
        console.log(iframeDiv.scrollTop + '/' + scrollTarget);
        iframe.style.height = (iframe.offsetHeight + 500) + 'px';
        // iframeDiv.scrollTo({
        //     top: scrollTarget,
        // });
    }
}

function insertContent(content, type, col, row) {
    let elemID = `c${col}r${row}`;
    // console.log(elemID);
    var elem = document.getElementById(elemID);

    elem.innerHTML = content;

    if (type === 'PDF') {
        let original_div = document.getElementById('pdf-div');
        let original_iframe = document.getElementById('pdf-iframe');
        let newID_div = `pdf-div-${elemID}`;
        let newID_iframe = `pdf-iframe-${elemID}`;
        original_div.id = newID_div;
        original_iframe.id = newID_iframe;
    }
}

function requestChangePreset(socket, session_id, p) {
    console.log("Request to Preset: " + p);
    socket.emit('request-change-preset', session_id, p);
}

function fillPresetDivs(session_id, socket, preset_objs) {
    for (let c = 0; c < preset_objs.length; c++) {
        for (let r = 0; r < preset_objs[c].length; r++) {
            switch (preset_objs[c][r]) {
                case BLANK:
                    socket.emit("chungus-request-template", {'session_id': session_id, 'uri': blank_uri, 'type': 'BLANK', 'row': r+1, 'col': c+1});
                    break;
                case PDF:
                    socket.emit("chungus-request-template", {'session_id': session_id, 'uri': sample_pdf_uri, 'type':'PDF', 'row': r+1, 'col': c+1});
                    break;
                case SPOTIFY:
                    break;
                default:
                    break;
            }
        }
    }
}

function dummyPrint(string) {
    console.log(string);
}


// The Browser API key obtained from the Google API Console.
// Replace with your own Browser API key, or your own key.
var developerKey = 'AIzaSyArcicIi3Dpg9lgMVNskGvXGoyACMGqtKM';

// The Client ID obtained from the Google API Console. Replace with your own Client ID.
var clientId = "673944149019-84nhe41bnt9d98chugu9uujlu2jnskgt.apps.googleusercontent.com"

// Replace with your own project number from console.developers.google.com.
// See "Project number" under "IAM & Admin" > "Settings"
var appId = "673944149019";

// Scope to use to access user's Drive items.
var scope = ['https://www.googleapis.com/auth/drive.file'];

var pickerApiLoaded = false;
var oauthToken;
var fileURL = "http://www.africau.edu/images/default/sample.pdf";

// Use the Google API Loader script to load the google.picker script.
function nosePicker(socket, session_id, c, r) {
    boogerPicker();
    function boogerPicker() {
        console.log("I AM PICKING BOOGERS");
        gapi.load('auth', {'callback': onAuthApiLoad});
        gapi.load('picker', {'callback': onPickerApiLoad});
    }

    function onAuthApiLoad() {
        window.gapi.auth2.authorize(
            {
            'client_id': clientId,
            'scope': scope,
            'immediate': false
            },
            handleAuthResult);
    }

    function onPickerApiLoad() {
        pickerApiLoaded = true;
        createPicker();
    }

    function handleAuthResult(authResult) {
        if (authResult && !authResult.error) {
        oauthToken = authResult.access_token;
        createPicker();
        }
    }

    // Create and render a Picker object for searching images.
    function createPicker() {
        if (pickerApiLoaded && oauthToken) {
        var view = new google.picker.View(google.picker.ViewId.DOCS);
        view.setMimeTypes("image/png,image/jpeg,image/jpg,application/pdf,application/msword,text/plain");
        var picker = new google.picker.PickerBuilder()
            .enableFeature(google.picker.Feature.NAV_HIDDEN)
            .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
            .setAppId(appId)
            .setOAuthToken(oauthToken)
            .addView(view)
            .addView(new google.picker.DocsUploadView())
            .setDeveloperKey(developerKey)
            .setCallback(pickerCallback)
            .build();
            picker.setVisible(true);
        }
    }

    // A simple callback implementation.
    function pickerCallback(data) {
        if (data.action == google.picker.Action.PICKED) {
            fileURL = data.docs[0].embedUrl;
            // alert('You Have Selected: ' + fileURL);
            socket.emit("smol-request-pdf", session_id, fileURL, c, r);
        }
    }

}
