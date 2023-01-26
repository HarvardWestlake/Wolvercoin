import React from "react";
import { Web3Context } from "../Contexts/Web3Provider";
import "./publicgoods.css";

const Auction = () => {
    const web3Context = React.useContext(Web3Context);

    const provider = web3Context.provider;
    const signer = provider.getSigner();
    const connectedPublicGoods = web3Context.publicGoodsContract.connect(signer);
    
    const [publicGoods, setPublicGoods] = React.useState({});

    React.useEffect(() => {
        async function fetchData() {
            let activeGoods = await connectedPublicGoods.getActiveGoods();
            const res = await Promise.all(activeGoods.map(async goodNumber => {
                const goal = await connectedPublicGoods.getGoal(goodNumber);
                const newPublicGoods = {...publicGoods};
                newPublicGoods[goodNumber] = {
                    goal: goal.toNumber()
                };
                setPublicGoods(newPublicGoods);
            }));
            console.log(res)
        }
        fetchData();
    }, [connectedPublicGoods]);
    
    return (
        <div className="public_goods">
            <h1>Public Goods</h1>
            <ul>
                <li>Contribute some WVC to each public good!</li>
                <li>Public goods benefit the whole class, e.g. Top T doing a dare or an ice cream party.</li>
                <li>If people donate enough money so that the goal is met, the public good happens.</li>
            </ul>
            <div id="goods_list">
                {
                    Object.keys(publicGoods).map(goodNumber => {
                        const good = publicGoods[goodNumber];
                        return (
                            <div className="good">
                                <h2>Public Good #{goodNumber}</h2>
                                <p>Goal: {good.goal}</p>
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Auction;
