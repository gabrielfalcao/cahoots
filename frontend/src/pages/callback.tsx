import React, { Component } from "react";
import { connect } from "react-redux";

import { Redirect } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
// import * as toastr from "toastr";

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
                this.props.setUser(user);
            })
            .catch(error => {
                console.log(error);
            });
    }

    render() {
        const { auth }: any = this.props;
        if (auth.profile) {
            return <Redirect to="/" />;
        }

        return (
            <Container fluid="md">
                <br />
                <br />
                <br />
                <br />

                <Row className="justify-content-md-center">
                    <Col md={6}>
                        <p>redirecting...</p>
                        <Spinner animation="border" role="status">
                            <span className="sr-only">
                                login authorized, you are being redirected
							</span>
                        </Spinner>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default connect(
    state => {
        return { ...state };
    },
    {
        setUser: function(user: any) {
            return {
                type: "NEW_AUTHENTICATION",
                user
            };
        }
    }
)(OAuth2Callback);
