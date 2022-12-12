import React from "react";
import * as Constants from "./consts"

class Nav extends React.Component {
    constructor(props) {
        super(props);
        this.getHashLocation = this.getHashLocation.bind(this);
    }

    componentDidMount() {
        if (window.location.hash) {
            let hash = window.location.hash.substring(1);
            this.props.updateHashLocation(hash);
        }
    }

    getHashLocation(e) {
        if (!e || !e.target || !e.target.name) {
          e = {target:{name:""}};
        }
        window.location.hash = e.target.name;
        this.props.updateHashLocation(e.target.name);
    }

  generateBarComparisonImages() {
    let navigationOptions = <div className="menu-items"></div>;
    let location = this.props.location ? this.props.location : Constants.NAV_DEFAULT_LOCATION;
    if (Object.keys(Constants.NAV_OPTIONS).length > 0) {
        navigationOptions = Object.keys(Constants.NAV_OPTIONS).map((key) => (
            <a key={key}  id={Constants.NAV_OPTIONS[key]} className={location == Constants.NAV_OPTIONS[key] ? "menu-item active" : "menu-item"} name={Constants.NAV_OPTIONS[key]} onClick={this.getHashLocation}>{key}</a>
      ));
    }
    return navigationOptions;
  }
    render() {
      let navOptions = this.generateBarComparisonImages();
      return (
        <div className="menu-items">
           {navOptions}
      </div>
      )
    }
};

export default Nav;