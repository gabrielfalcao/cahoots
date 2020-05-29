import React, { Component } from "react";
import PropTypes from "prop-types";

import {
    BrowserRouter as Router,
    Route,
    Switch,
    Redirect
} from "react-router-dom";
/* import { NavLink } from "react-router-dom";*/
// import { ComponentWithStore } from "./ui";

import { LinkContainer } from "react-router-bootstrap";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";

import ProfilePage from "./pages/home";
import TemplateAdmin from "./pages/TemplateAdmin";
import OAuth2Callback from "./pages/callback";
import Login from "./pages/login";
import Logout from "./pages/logout";
import { ComponentWithStore } from "./ui";

type AppState = {
    user: any;
    error: Error | null;
};
type AppProps = {
    auth: any;
};

function needs_login(auth: any) {
    if (!auth) {
        return true;
    }
    if (!auth.scope) {
        return true;
    }
    return typeof auth.scope !== "string";
}

class App extends Component<AppProps, AppState> {
    static propTypes = {
        auth: PropTypes.object
    };
    render() {
        const { auth } = this.props;

        function AuthenticatedRoute({
            children,
            ...rest
        }: {
            [key: string]: any;
        }) {
            return (
                <Route
                    {...rest}
                    render={({ location }) =>
                        !needs_login(auth) ? (
                            children
                        ) : (
                                <Redirect
                                    to={{
                                        pathname: "/login",
                                        state: { from: location }
                                    }}
                                />
                            )
                    }
                />
            );
        }

        return (
            <Router>
                <Navbar bg="light" expand="lg" sticky="top">
                    <LinkContainer to="/">
                        <Navbar.Brand>Fake NOM</Navbar.Brand>
                    </LinkContainer>
                    <Navbar.Toggle aria-controls="fakenom-navbar-nav" />

                    <Navbar.Collapse
                        className="justify-content-end"
                        id="fakenom-navbar-nav"
                    >
                        <Nav>
                            {needs_login(auth) ? (
                                <LinkContainer to="/login">
                                    <Nav.Link>Login</Nav.Link>
                                </LinkContainer>
                            ) : (
                                    <React.Fragment>
                                        <LinkContainer to="/profile">
                                            <Nav.Link>Home</Nav.Link>
                                        </LinkContainer>

                                        <LinkContainer to="/admin">
                                            <Nav.Link>Template API Admin</Nav.Link>
                                        </LinkContainer>

                                        <Nav.Link href="/api">
                                            Fake NewStore API v1
									</Nav.Link>

                                        <LinkContainer to="/logout">
                                            <Nav.Link>Logout</Nav.Link>
                                        </LinkContainer>
                                    </React.Fragment>
                                )}
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
                <Switch>
                    <Route path="/oauth2/callback">
                        <OAuth2Callback />
                    </Route>
                    <Route path="/login">
                        <Login />
                    </Route>
                    <Route path="/logout">
                        <Logout />
                    </Route>
                    <Route exact path="/">
                        <Redirect to="/admin" />
                    </Route>
                    <AuthenticatedRoute path="/profile">
                        <ProfilePage />
                    </AuthenticatedRoute>
                    <AuthenticatedRoute path="/admin">
                        <TemplateAdmin />
                    </AuthenticatedRoute>
                </Switch>
            </Router>
        );
    }
}
export default ComponentWithStore(App);
