import React, { Component } from "react";
import { connect } from "react-redux";

import { Redirect } from "react-router-dom";
import Container from "react-bootstrap/Container";
import * as toastr from "toastr";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Spinner from "react-bootstrap/Spinner";
import { AuthService } from "../auth";

type CallbackProps = {
    setUser: any;
};
type CallbackState = {
    user: any;
};

class OAuth2Callback extends Component<CallbackProps, CallbackState> {
    public authService: AuthService;

    constructor(props: any) {
        super(props);

        this.authService = new AuthService();
        this.state = { user: null };
    }

    public componentDidMount() {
        this.authService
            .handleCallback()
            .then(user => {
                this.setState({ user });
                this.props.setUser(user);
                console.log("callback user", user);
                toastr.info(`callback succeedded`);
            })
            .catch(error => {
                toastr.error(error);
            });
    }

    render() {
        const { user } = this.state;
        console.log(user);
        if (user !== null) {
            return <Redirect to="/" />;
        }

        return (
            <Container>
                <Row>
                    <Col>
                        <br />
                        <br />
                        <br />
                        <br />

                        <Spinner animation="border" role="status">
                            <span className="sr-only">Loading...</span>
                        </Spinner>
                    </Col>
                </Row>
            </Container>
        );
    }
}

function setUser(user: any) {
    return {
        type: "NEW_AUTHENTICATION",
        user
    };
}
export default connect(
    state => {
        return { ...state };
    },
    { setUser }
)(OAuth2Callback);
