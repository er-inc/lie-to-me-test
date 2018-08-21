import React from 'react';
import Webcam from './Webcam';
import RecordRTC from 'recordrtc';

const hasGetUserMedia = !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
                        navigator.mozGetUserMedia || navigator.msGetUserMedia);

class RecordPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      recordVideo: null,
      src: null,
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
    navigator.getUserMedia({ audio: false, video: true }, callback, (error) => {
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

    setTimeout(() => {
      this.stopRecord();
    }, 4000);
  }

  stopRecord() {
    this.state.recordVideo.stopRecording(() => {
      this.state.recordVideo.save('Test');
    });
  }

  saveBlob(blob, fileName) {
    console.log("saving blob");
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    return (blob, fileName) => {
      var url = window.URL.createObjectURL(blob);
      a.href = url;
      a.download = fileName;
      a.click();
      window.URL.revokeObjectURL(url);
    };
  }

  render() {
    return(
      <div>
        <div><Webcam src={this.state.src}/></div>
        <div><button onClick={this.startRecord}>Start Record</button></div>
      </div>
    )
  }
}

export default RecordPage;
