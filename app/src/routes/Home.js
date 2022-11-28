import React from "react";
import Header from "../components/Common/Header.js";
import Footer from "../components/Common/Footer.js";
/*
import Options from "../components/Home/Options.js";
import Numbers from "../components/Home/Numbers.js";
import Roadmap from "../components/Home/Roadmap.js";
*/
import "../components/Common/main.css";

class Home extends React.Component {
  state = {
    count: this.props.count || 0,
  };
  componentDidMount() {
    const { drizzle } = this.props;
    const contract = drizzle.contracts.Reimbursement;
const dataKey = null;
    // get and save the key for the variable we are interested in
    //const dataKey = contract.methods["storedData"].cacheCall();
    this.setState({ dataKey });
  }

  render() {
    const { count } = this.state;

    //const { SimpleStorage } = this.props.drizzleState.contracts;
    //const storedData = SimpleStorage.storedData[this.state.dataKey];
    //return <DisplayValue value={storedData && storedData.value} />;
    return (
      <div>
        <Header />
        
        <Footer />
      </div>
    );
  }
}

export default Home;
