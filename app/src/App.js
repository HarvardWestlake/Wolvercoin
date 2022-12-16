
import './App.css';
import Main from './components/Main/main'
import React from "react";
import { Web3Provider } from './components/Contexts/Web3Provider';
import { ethers } from "ethers";
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  async getProvider() {

    const provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
    console.log(provider);
    return provider;
  }
  render() {
    const provider = this.getProvider();
    return (
      <div className="App">
        <Web3Provider provider={provider}>
          <Main />
        </Web3Provider>
      </div>
    );
  }
}

export default App;
