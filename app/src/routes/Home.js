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

  render() {
    const { count } = this.state;

    return (
      <div>
        <Header />
        <Footer />
      </div>
    );
  }
}

export default Home;
