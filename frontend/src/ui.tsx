import { connect } from "react-redux";
/* import { withRouter } from "react-router-dom"
 * */

export function ComponentWithStore(Component: any) {
    return connect(
        state => {
            return { ...state };
        },
        dispatch => {
            return {};
        }
    )(Component);
}
