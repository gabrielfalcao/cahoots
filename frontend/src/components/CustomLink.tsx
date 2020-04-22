import React from "react";
import { useStyletron } from "baseui";

export default function() {
    const [css, theme] = useStyletron();
    return (
        <a
            href="/my-link"
            className={css({
                fontSize: "20px",
                color: theme.colors.primary
            })}
        >
            Custom Link
        </a>
    );
}
