const base_url = "http://127.0.0.1:5000";
const INITIAL_PRESET = 2;
const sample_pdf_uri = "sample_pdf.html";
const blank_uri = "blank.html";

const BLANK = Symbol("BLANK");
const PDF = Symbol("PDF");
const SPOTIFY = Symbol("SPOTIFY");

var presets = {
    1: [[BLANK, BLANK]],
    2: [[BLANK, PDF]]
}

function bodyOnload() {
    var webpage = window.location.href;
    console.log("Page Loaded: " + webpage);
    if (webpage.indexOf('chungus') !== -1) {
        chungusInit();
    }
    else if (webpage.indexOf('display_testing') !== -1) {
        displayInit();
    }
}

// This was necessary for Chungus scrolling to work correctly. Figure out how to not use this!!
// function iframeOnload() {
//     bodyOnload();
// }

function displayInit() {
    console.log("Page Init: Display Testing");
    var socket = io.connect(base_url);
    socket.on('connect', function() {
        socket.emit("display-testing-ready", "Display Testing: User has connected.")
    });

    var preset;

    socket.on("display-init", function(msg) {
        preset = INITIAL_PRESET; // Initial preset on launch is 1
        var page = document.getElementById("display-page");
        page.innerHTML = msg[1];

        socket.on("display-template-response", function(msg) {
            insertContent(msg['content'], msg['type'], msg['row'], msg['col']);
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
        let preset_objs = presets[preset];
        for (let r = 0; r < preset_objs.length; r++) {
            for (let c = 0; c < preset_objs[r].length; c++) {
                switch (preset_objs[r][c]) {
                    case BLANK:
                        socket.emit("display-request-template", {'uri': blank_uri, 'type': 'BLANK', 'row': r+1, 'col': c+1});
                        break;
                    case PDF:
                        socket.emit("display-request-template", {'uri': sample_pdf_uri, 'type':'PDF', 'row': r+1, 'col': c+1});
                        break;
                    case SPOTIFY:
                        break;
                    default:
                        break;
                }
            }
        }
        
    });

}

function chungusInit() {
    console.log("Page Init: Chungus");
    var socket = io.connect(base_url);
    socket.on('connect', function() {
        socket.emit("chungus-ready", 'Chungus: User has connected.');
    });

    // Listen for pdf scroll from Flask App
    socket.on('pdf-scroll-event', function(msg) {
        // console.log(msg);
        if (msg[0] === 'Down') {
            pdfScroll(msg[1], 0)
        }
        else if (msg[0] === 'Up') {
            pdfScroll(msg[1], 1)
        }
    });
}

function pdfScroll(row_col, dir) {
    let frame_name = `pdf-iframe-${row_col}`;
    let div_name = `pdf-div-${row_col}`;
    var iframe = document.getElementById(frame_name);
    var iframeDiv = document.getElementById(div_name);
    if (iframeDiv === null || iframe === null) return;

    console.log("Attempting to scroll " + row_col);
    
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
        iframeDiv.scrollTo({
            top: scrollTarget,
        });
    }
}

function insertContent(content, type, row, col) {
    let elemID = `r${row}c${col}`;
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