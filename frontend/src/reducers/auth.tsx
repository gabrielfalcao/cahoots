import jwt_decode from "jwt-decode";

const DEFAULT_STATE = {};

export const auth = (state: any = DEFAULT_STATE, action: any = {}) => {
    switch (action.type) {
        case "NEW_AUTHENTICATION":
            let { user } = action;
            let {
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
                user: action.user,
                id_token: jwt_decode(id_token),
                access_token: jwt_decode(access_token),
                refresh_token: jwt_decode(refresh_token)
            };

        case "LOGOUT":
            return {};
        default:
            return { ...state };
    }
};

export default auth;
