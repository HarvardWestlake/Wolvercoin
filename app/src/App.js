
import './App.css';
import Main from './components/Main/main'
import React from "react";
import { Web3Provider } from './components/Contexts/Web3Provider';
import {ethers} from "ethers";
import {Web3Context} from "./components/Contexts/Web3Provider"


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

        <Web3Context.Consumer>
            {providerValueContext => { 
              return <Main provider={this.state.provider} web3Context={providerValueContext}/>
            }}
          </Web3Context.Consumer>
          
        </Web3Provider>
      </div>
    );
  }
}

export default App;
