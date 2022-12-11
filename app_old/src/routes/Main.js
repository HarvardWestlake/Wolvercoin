import React, { lazy } from "react";
import "../components/Common/main.css";
import "../components/Contribute/main.css"
import NFTAddition from "../components/Contribute/NFTAddition";
import Firestore from "../components/Firebase/Firestore.js";
import { Web3Context, withWeb3 } from "../components/Web3"
import Header from "../components/Common/Header/main"
import Footer from "../components/Common/Footer"


const ContributeRoute = lazy(() => import("./Contribute.js"));

class Main extends React.Component {
    constructor(props) {
        super(props);
        this.getSelectedNavContent = this.getSelectedNavContent.bind(this);
    }
  componentDidMount() {
    //const contract = drizzle.contracts.Reimbursement;
    const dataKey = null;
    // get and save the key for the variable we are interested in
    //const dataKey = contract.methods["storedData"].cacheCall();
    this.setState({ dataKey });
  }

  uploadToIPFS() {
     alert('button clicked');
  }

  getSelectedNavContent() {
    let content = '';
    // grab url
    // find #tag and switch
    content = <ContributeRoute firestore={Firestore} />;
    return content
  }

  render() {
    const { count } = this.state;

    const activeContent = this.getSelectedNavContent();
    //const { SimpleStorage } = this.props.drizzleState.contracts;
    //const storedData = SimpleStorage.storedData[this.state.dataKey];
    //return <DisplayValue value={storedData && storedData.value} />;
    return (
      <div>
        <Header val={this.props.web3Context}/> 
        {activeContent}
        <Footer />
      </div>
    );
  }
}

export default Main;
