import { createStore, applyMiddleware, compose } from "redux";

import rootReducer from "./reducers";
import { save, load } from "redux-localstorage-simple";

const composeEnhancers =
    (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const loaded = load({ namespace: "fakenom.state" });
console.log("loaded storage", loaded);
export default createStore(
    rootReducer,
    loaded,
    composeEnhancers(applyMiddleware(save({ namespace: "fakenom.state" })))
);
