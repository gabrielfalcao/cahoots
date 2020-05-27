import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";

import Home from "./pages/home";
import OAuth2Callback from "./pages/callback";
import Login from "./pages/login";
import Logout from "./pages/logout";

export default function App() {
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
                    <Nav className="mr-auto">
                        <LinkContainer to="/">
                            <Nav.Link>Home</Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/login">
                            <Nav.Link>Login</Nav.Link>
                        </LinkContainer>
                        <LinkContainer to="/logout">
                            <Nav.Link>Logout</Nav.Link>
                        </LinkContainer>
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
                <Route path="/Logout">
                    <Logout />
                </Route>
                <Route path="/">
                    <Home />
                </Route>
            </Switch>
        </Router>
    );
}
