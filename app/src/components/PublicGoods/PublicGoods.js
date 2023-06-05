import React from "react";
import { Web3Context } from "../Contexts/Web3Provider";
import PublicGoodItem from "./PublicGoodItem";
import "./publicgoods.css";

const PublicGoods = () => {
    
    const [publicGoods, setPublicGoods] = React.useState({});
    const [connectedPublicGoods, setConnectedPublicGoods] = React.useState(null);
    const [connectedNft, setConnectedNft] = React.useState(null);
    const [connectedWolvercoin, setConnectedWolvercoin] = React.useState(null);

    const web3Context = React.useContext(Web3Context);
    
    React.useEffect(() => {
        const provider = web3Context?.provider;
        const signer = provider?.getSigner();
        setConnectedPublicGoods(web3Context?.publicGoodsContract.connect(signer));
        setConnectedNft(web3Context?.nftContract.connect(signer));
        setConnectedWolvercoin(web3Context?.wolvercoinContract.connect(signer));
    }, [web3Context]);

    const fetchData = React.useCallback(async () => {
        if(!connectedPublicGoods) return;
        let activeGoods = await connectedPublicGoods.getActiveGoods();
        const newPublicGoods = {};
        await Promise.all(activeGoods.map(async goodNumber => {
            const goal = await connectedPublicGoods.getGoal(goodNumber);
            const total = await connectedPublicGoods.getContributionTotal(goodNumber);
            const name = await connectedPublicGoods.getName(goodNumber);
            const creator = await connectedPublicGoods.getCreator(goodNumber);
            newPublicGoods[goodNumber] = {
                goal: goal.toNumber(),
                total: total.toNumber(),
                name,
                creator,
                nftUrl: await connectedNft.tokenURI(goodNumber)
            };
        }));
        setPublicGoods(newPublicGoods);
    }, [connectedNft, connectedPublicGoods]);

    React.useEffect(() => {
        console.log("Fetchdata")
        fetchData();
    }, [connectedPublicGoods, connectedNft, fetchData]);
    
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
                            <PublicGoodItem
                                key={goodNumber}
                                goodNumber={goodNumber}
                                good={good}
                                connectedPublicGoods={connectedPublicGoods}
                                connectedWolvercoin={connectedWolvercoin}
                                refresh={fetchData}
                            />
                        )
                    })
                }
            </div>
        </div>
    )
}

export default PublicGoods;
