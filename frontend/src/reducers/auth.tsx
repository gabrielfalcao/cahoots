// import jwt_decode from "jwt-decode";

const DEFAULT_STATE = {};

export const auth = (state: any = DEFAULT_STATE, action: any = {}) => {
    switch (action.type) {
        case "NEW_AUTHENTICATION":
            const { user } = action;
            const {
                id_token,
                access_token,
                refresh_token,
                scope,
                profile
            } = user;
            return {
                ...state,
                scope,
                profile,
                id_token,
                access_token,
                refresh_token
            };

        case "LOGOUT":
            return {
                scope: null,
                profile: null,
                id_token: null,
                access_token: null,
                refresh_token: null
            };
        default:
            return { ...state };
    }
};

export default auth;
