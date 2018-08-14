/* eslint-disable */
import videojs from 'video.js';
import 'webrtc-adapter';

/*
// the following imports are only needed when you're recording
// audio-only using the videojs-wavesurfer plugin
import WaveSurfer from 'wavesurfer.js';
import MicrophonePlugin from 'wavesurfer.js/dist/plugin/wavesurfer.microphone.js';
WaveSurfer.microphone = MicrophonePlugin;

// register videojs-wavesurfer plugin
import 'videojs-wavesurfer/dist/css/videojs.wavesurfer.css';
import Wavesurfer from 'videojs-wavesurfer/dist/videojs.wavesurfer.js';
*/

// register videojs-record plugin with this import
import Record from 'videojs-record/dist/videojs.record.js';

var player;
const elementId = 'myVideo';
const playerOptions = {
    controls: true,
    autoplay: false,
    fluid: false,
    loop: false,
    width: 320,
    height: 240,
    controlBar: {
        volumePanel: false
    },
    plugins: {
        // configure videojs-record plugin
        record: {
            audio: false,
            video: true,
            debug: true
        }
    }
};

// wait till DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // create player
    player = videojs(elementId, playerOptions, function() {
        console.log('player ready! id:', elementId);
        // print version information at startup
        var msg = 'Using video.js ' + videojs.VERSION +
            ' with videojs-record ' + videojs.getPluginVersion('record') +
            ' and recordrtc ' + RecordRTC.version;
        videojs.log(msg);
    });

    // device is ready
    player.on('deviceReady', function() {
        console.log('device is ready!');
    });

    // user clicked the record button and started recording
    player.on('startRecord', function() {
        console.log('started recording!');
    });

    // user completed recording and stream is available
    player.on('finishRecord', function() {
        // the blob object contains the recorded data that
        // can be downloaded by the user, stored on server etc.
        console.log('finished recording: ', player.recordedData);
    });
});
