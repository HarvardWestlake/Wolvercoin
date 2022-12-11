import React from "react";

class HeaderNavigation extends React.Component {
  componentDidMount() {
    console.log(this.props);
  }

  highlightSelectedRoute() {
    console.log(window.location);
  }


  render() {
    return (
        <div></div>
    ) 
  }
};


export default HeaderNavigation;
