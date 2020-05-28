const INITIAL_EMPTY_STATE = {
    all: [],
    filtered: [],
    loaded: false
};

export const templates = (
    state: any = INITIAL_EMPTY_STATE,
    action: any = {}
) => {
    let filtered;
    let all_templates;

    switch (action.type) {
        case "LOGOUT":
        case "UNLOAD_TEMPLATES":
            return { ...INITIAL_EMPTY_STATE };

        case "SET_TEMPLATES":
            return {
                ...state,
                filtered: filtered,
                all: all_templates,
                loaded: true,
                error: action.error || null
            };

        case "LOADING_TEMPLATES":
            return { ...state, loaded: false, current: null };

        case "CHANGE_TEMPLATE":
            return {
                ...state,
                current: action.template,
                error: action.error,
                loaded: true
            };

        default:
            return { ...state };
    }
};

export default templates;
