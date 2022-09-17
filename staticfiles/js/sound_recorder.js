const display = document.querySelector('.display')
const controllerWrapper = document.querySelector('.controllers')
const subtitles_textarea = document.getElementById('subtitles_text_area')
const form_subtitles = document.getElementById('form_subtitles')
const words_counter = document.getElementById('words_counter')
const audio_lenght = document.getElementById('audio_lenght')
const words_per_second = document.getElementById('words_per_second')


var words_counter_int = 0
var audio_lenght_int = 0
var words_per_second_int = 0

const State = ['Initial', 'Record', 'Download', 'After_get_subtitles']
let stateIndex = 0
let mediaRecorder, chunks = [], audioURL = ''

var blob = new Blob()

//stopwatch
  var seconds = 00; 
  var tens = 00; 
  var Interval ;
  function triger_stopwatch_start(){
    clearInterval(Interval);
    Interval = setInterval(startTimer, 10);
  }
  function triger_stopwatch_stop(){
    clearInterval(Interval);
  }
  function startTimer () {
    tens++; 
    var appendTens = document.getElementById("tens")
    var appendSeconds = document.getElementById("seconds")
    if(tens <= 9){
      appendTens.innerHTML = "0" + tens;
    }
    if (tens > 9){
      appendTens.innerHTML = tens;
      
    } 
    if (tens > 99) {
      //console.log("seconds");
      seconds++;
      appendSeconds.innerHTML = "0" + seconds;
      tens = 0;
      appendTens.innerHTML = "0" + 0;
    }
    if (seconds > 9){
      appendSeconds.innerHTML = seconds;
    }
  }
  

// █▀█ █▀▀ █▀▀ █▀█ █▀█ █▀▄ █▀▀ █▀█ 
// █▀▄ ██▄ █▄▄ █▄█ █▀▄ █▄▀ ██▄ █▀▄ 
// mediaRecorder setup for audio
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    //console.log('mediaDevices supported..')
    navigator.mediaDevices.getUserMedia({
        audio: true
    }).then(stream => {
        mediaRecorder = new MediaRecorder(stream)
        // this is recorders start
        mediaRecorder.ondataavailable = (e) => {
            chunks.push(e.data)
        }
        // this is recorders stop
        mediaRecorder.onstop = () => {
            blob = new Blob(chunks, {'type': 'audio/ogg; codecs=opus'})
            //blob = new Blob(chunks, {'type': 'audio/mp3'})
            chunks = []
            audioURL = window.URL.createObjectURL(blob)
            document.querySelector('audio').src = audioURL
            document.querySelector('audio').download = 'odf_name'
        }
    }).catch(error => {
        console.log('Following error has occured : ',error)
    })
}else{
    stateIndex = ''
    application(stateIndex)

}

//workers
const record = () => {
    form_subtitles.style.display = "none";
    stateIndex = 1
    mediaRecorder.start()
    clearInterval(Interval);
    application(stateIndex)
    seconds = 00; 
    tens = 00; 
}

const stopRecording = () => {
    stateIndex = 2
    mediaRecorder.stop()
    clearInterval(Interval);
    application(stateIndex)
    seconds = 00; 
    tens = 00; 

}

const downloadAudio = () => {
    const downloadLink = document.createElement('a')
    downloadLink.href = audioURL
    console.log(audioURL)
    downloadLink.setAttribute('download', 'audio')
    downloadLink.click()
}




// ▀█▀ █▄ █ ▀█▀ ▀█▀ ▀█▀ ▄▀▄ █   
// ▄█▄ █ ▀█ ▄█▄  █  ▄█▄ █▀█ █▄▄

//remove all the content inside display and controllerWrapper.
const clearDisplay = () => {
    display.textContent = ''
}

//remove all the content inside display and controllerWrapper.
const clearControls = () => {
    controllerWrapper.textContent = ''
}

//addMessage() appends a <p> tag inside display with text
const addMessage = (text) => {
    const msg = document.createElement('p')
    msg.textContent = text
    display.append(msg)
}



//addButton() appends <button> tag to controllerWrapper with an onclick attribute.
const addButton = (id, funString, text) => {
    const btn = document.createElement('button')
    btn.className = "button-74";
    btn.id = id
    btn.setAttribute('onclick', funString)
    btn.textContent = text
    btn.style.cssText = 'margin-right:15px;';
    controllerWrapper.append(btn)
}

//addAudio() creates an <audio> tag inside display.
const addAudio = () => {
    const audio = document.createElement('audio')
    //audio.className = "audioplayer";
    audio.controls = true
    audio.src = audioURL
    audio.type = 'blobType'
    display.append(audio)
    
    // $(function() {
    //     $('audio').audioPlayer();
    // });
}

const add_stopwatch = () => {
    const stopwatch = document.createElement('p')
    stopwatch.innerHTML = '<span id="seconds">00</span>:<span id="tens">00</span>'
    display.append(stopwatch)
}

// Generate subtitles
function subtitle_generator_initialize() {
    document.getElementById('loading_circle').style.display = "block";
    setTimeout(subtitle_generator_ajax, 500);
}


function subtitle_generator_ajax (){
    console.log(question_pk)
    var temp_name = "temp" + user_pk + ".mp3"
    //var url = (window.URL || window.webkitURL).createObjectURL(blob);
    var file = new File([ blob ], temp_name, { type: "audio/mp3"} );
    //var file = new File([ blob ], "temp.mp3", { type: "audio/mp3"} );

    var data = new FormData();
    //data.append('audio_file', blob);
    data.append('question_pk', question_pk);
    data.append('file',file);

    $.ajax({
        url :  "/subtitle_generator/",
        type: 'POST',
        data: data,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log('success')
            loading_circle.style.display = "none";
            //("success!");
            words_counter.innerHTML= data['words_counter']
            audio_lenght.innerHTML= data['audio_lenght']
            words_per_second.innerHTML= data['words_per_second']
        
            words_counter_int = data['words_counter']
            audio_lenght_int = data['audio_lenght']
            words_per_second_int = data['words_per_second']
            // {{}}
            // {{}} seconds
            //  {{}}
            form_subtitles.style.display = "block";

            subtitles_textarea.value = data['subtitles']
            stateIndex = 3
            application(stateIndex)
            //var get_subtitles_button = document.getElementById('get_subtitles')
            //get_subtitles_button.display = "none";
        },    
        error: function() {
            loading_circle.style.display = "none";
            console.log('fail')
            //alert("fail!");
        }
    });
}


function save_audio_answer (){
    edited_subtitles = subtitles_textarea.value
    var check_box_share = document.getElementById('toggle2').checked;
    var question_slug = document.getElementById('question_slug').value;
    
    var temp_name = "temp" + user_pk + ".mp3"
    var file = new File([ blob ], temp_name, { type: "audio/mp3"} );
    //var file = new File([ blob ], "temp.mp3", { type: "audio/mp3"} );

    var data = new FormData();
    //data.append('audio_file', blob);
    data.append('question_pk', question_pk);
    data.append('file',file);
    data.append('edited_subtitles',edited_subtitles);
    data.append('check_box_share',check_box_share);
    data.append('words_counter_int',words_counter_int);
    data.append('audio_lenght_int',audio_lenght_int);
    data.append('words_per_second_int',words_per_second_int);

    $.ajax({
        url :  "/save_audio_answer/",
        type: 'POST',
        data: data,
        contentType: false,
        processData: false,
        success: function(data) {
            if (data["status"] == "fail") {
                console.log(123)
                window.location.replace("/question_detailed/"+question_slug + "?answer_fail=fail");
            }
            else {
                loading_circle.style.display = "none";
                form_subtitles.style.display = "block";
                window.location.replace("/question_detailed/"+data['question_slug']+ "?ans_pk=" + data['answer_pk'] +"&del=2#" + data['answer_pk']);
            }
        },    
        error: function() {
            loading_circle.style.display = "none";
        }
    });
}

// Save audio file answer with subtitles
function save_audio_answer_initialize() {
    console.log("we aresave_audio_answerse save_audio_answer")
    document.getElementById('loading_circle').style.display = "block";
    setTimeout(save_audio_answer, 500);
}

const application = function (index) {
    switch (State[index]) {
        case 'Initial':
            clearDisplay()
            clearControls()
    
            addMessage('Press the start button to start recording')
            addButton('record', 'record()', 'Start Recording')
            break;

        case 'Record':
            clearDisplay()
            clearControls()

            addMessage('Recording...')
            add_stopwatch()
            triger_stopwatch_start()
            addButton('stop', 'stopRecording()', 'Stop Recording')
            break

        case 'Download':
            clearControls()
            clearDisplay()

            addAudio()
            addButton('get_subtitles', 'subtitle_generator_initialize()', 'Get subtitles')
            //addButton('download', 'downloadAudio()', 'Download Audio')
            addButton('record', 'record()', 'Record Again')
            triger_stopwatch_stop()
            break


        case 'After_get_subtitles':
            clearControls()
            clearDisplay()

            addAudio()
            //addButton('download', 'downloadAudio()', 'Download Audio')
            addButton('record', 'record()', 'Record Again')
            triger_stopwatch_stop()
            break

        
        default:
            clearControls()
            clearDisplay()

            addMessage('Your browser does not support mediaDevices')
            break;
    }
}

application(stateIndex)


