import React from "react";
import "../components/Common/main.css";
import "../components/Contribute/main.css"
import NFTAddition from "../components/Contribute/NFTAddition";


const POSSIBLE_NFT_UPLOAD_STATES = {
    SPLASH : "SPLASH",
    UPLOADING_TO_IPFS : "UPLOADING_TO_IPFS",
    UPLOADED_TO_IPFS : "UPLOADED_TO_IPFS"
};

class Contribute extends React.Component {
  state = {
    count: this.props.count || 0,
    nftProgress : POSSIBLE_NFT_UPLOAD_STATES.SPLASH
  };
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

  render() {
    const { count } = this.state;


    //const { SimpleStorage } = this.props.drizzleState.contracts;
    //const storedData = SimpleStorage.storedData[this.state.dataKey];
    //return <DisplayValue value={storedData && storedData.value} />;
    return (
      <div>
        <NFTAddition />
       Contribute Content
      </div>
    );
  }
}

export default Contribute;
