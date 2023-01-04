
import './App.css';
import Main from './components/Main/main'
import React from "react";
import { initializeApp } from 'firebase/app';
import { Web3Provider } from './components/Contexts/Web3Provider';

const firebaseConfig = {
  apiKey: "AIzaSyB13Rzp7Ey2IFI3RTY9cD1VHFq9p8_uF4U",
  authDomain: "wolvercoin-hw.firebaseapp.com",
  projectId: "wolvercoin-hw",
  storageBucket: "wolvercoin-hw.appspot.com",
  messagingSenderId: "101117958130",
  appId: "1:101117958130:web:49ad8f0613ef4eb66d3d6b",
  measurementId: "G-PC4QR208EF"
};

const app = initializeApp(firebaseConfig);
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  render() {
    return (
      <div className="App">
        <Web3Provider>
          <Main />
        </Web3Provider>
      </div>
    );
  }
}

export default App;
