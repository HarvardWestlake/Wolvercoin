
import './App.css';
import Main from './components/Main/main'
import React from "react";
import { Web3Provider } from './components/Contexts/Web3Provider';
import {ethers} from "ethers";



const getProvider = async() =>{
  const provider = ((window.ethereum != null) ? new ethers.providers.Web3Provider(window.ethereum) : ethers.providers.getDefaultProvider());
  return provider;
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      provider : null
    };
  }

  async componentDidMount() {
    var provider = await getProvider();
    console.log(provider);
    await this.setState({provider});
  }
  render() {
    return (
      <div className="App">
        <Web3Provider>
          <Main provider={this.state.provider}/>
        </Web3Provider>
      </div>
    );
  }
}

export default App;
