import React from "react";
import Header from "../components/Common/Header/main.js";
import Footer from "../components/Common/Footer.js";
import "../components/Common/main.css";

class Home extends React.Component {
  state = {
    count: this.props.count || 0,
  };
  componentDidMount() {
    //const contract = drizzle.contracts.Reimbursement;
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
       Main content
      </div>
    );
  }
}

export default Home;
