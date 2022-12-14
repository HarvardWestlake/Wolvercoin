
import './App.css';
import Main from './components/Main/main'
import { initializeApp } from 'firebase/app';

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
function App() {
  return (
    <div className="App">
        <Main></Main>
    </div>
  );
}

export default App;
