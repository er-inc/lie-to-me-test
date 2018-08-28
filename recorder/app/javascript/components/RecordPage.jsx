import React from 'react';
import Webcam from './Webcam';
import RecordRTC from 'recordrtc';

const hasGetUserMedia = !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
                        navigator.mozGetUserMedia || navigator.msGetUserMedia);

class RecordPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      startTimestamp: null,
      recordVideo: null,
      question_timestamps: [],
      answer_timestamps: [],
    };

    this.requestUserMedia = this.requestUserMedia.bind(this);
    this.startRecord = this.startRecord.bind(this);
    this.stopRecord = this.stopRecord.bind(this);
  }

  componentDidMount() {
    if(!hasGetUserMedia) {
      alert("Your browser cannot stream from your webcam. Please switch to Chrome or Firefox.");
      return;
    }
    this.requestUserMedia();
  }

  captureUserMedia(callback) {
    navigator.getUserMedia({ audio: true, video: true }, callback, (error) => {
      alert(JSON.stringify(error));
    });
  }


  requestUserMedia() {
    this.captureUserMedia((stream) => {
      this.setState({ src: window.URL.createObjectURL(stream) });
      console.log('setting state', this.state)
    });
  }

  startRecord() {
    this.captureUserMedia((stream) => {
      this.state.recordVideo = RecordRTC(stream, { type: 'video' });
      this.state.recordVideo.startRecording();
    });
    this.state.startTimestamp = new Date().getTime();
  }

  stopRecord() {
    this.state.recordVideo.stopRecording(() => {
      this.state.recordVideo.save('Test');
    });
  }

  startQuestion() {
    this.state.question_timestamps.push(getInfo(new Date().getTime() - this.state.startTimestamp));
  }

  startAnswer() {
    this.state.answer_timestamps.push(getInfo(new Date().getTime() - this.state.startTimestamp));
  }

  getInfo(milisecs) {
    var secs = milisecs / 1000;
    var min = Math.floor(secs / 60);
    var sec = Math.floor(secs - (min * 60));
    var milisec = milises % 1000;

    if (min < 10) {
      min = "0" + min;
    }

    if (sec < 10) {
      sec = "0" + sec;
    }

    return '${min}-${sec}';
  }

  render() {
    return(
      <div>
        <div><Webcam src={this.state.src}/></div>
        <div><button onClick={this.startRecord}>Start Record</button></div>
        <div><button onClick={this.stopRecord}>Stop Record</button></div>
        <div><button onClick={this.startQuestion}>Question Starts</button></div>
        <div><button onClick={this.startAnswer}>Answer Starts</button></div>
      </div>
    )
  }
}

export default RecordPage;
