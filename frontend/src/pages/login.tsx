import React, { Component } from "react";

import Container from "react-bootstrap/Container";
import * as toastr from "toastr";

import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Modal from "react-bootstrap/Modal";
import { AuthService } from "../auth";

// the clock's state has one field: The current time, based upon the
// JavaScript class Date
type LoginState = {
    user: any;
    error: Error | null;
};

export default class Login extends Component<{}, LoginState> {
    public authService: AuthService;
    private shouldCancel: boolean;

    constructor(props: any) {
        super(props);

        this.authService = new AuthService();
        this.shouldCancel = false;
        this.state = { user: null, error: null };
    }

    componentWillMount() {
        this.getUser();
    }
    public getUser = () => {
        this.authService
            .getUser()
            .then(user => {
                console.log("user", user);
                if (user) {
                    toastr.success(
                        "User has been successfully loaded from store."
                    );
                } else {
                    toastr.info("You are not logged in.");
                }

                if (!this.shouldCancel) {
                    this.setState({ user });
                }
            })
            .catch(error => {
                this.setState({ error });
            });
    };
    public login = () => {
        this.authService.login();
    };

    componentDidMount() { }

    render() {
        return (
            <Container fluid="md">
                <Row>
                    <Col md={12}>
                        <Modal.Dialog>
                            <Modal.Header>
                                <Modal.Title>
                                    You will be taken to KeyCloak
								</Modal.Title>
                            </Modal.Header>

                            <Modal.Body>
                                <p>
                                    Your user needs at least the scopes{" "}
                                    <code>template:read</code> or{" "}
                                    <code>template:write</code> to use the
									<a href="https://keycloak.fulltest.co">
                                        Fake NewStore API v1
									</a>
									.
								</p>
                            </Modal.Body>

                            <Modal.Footer>
                                <Button onClick={this.login} variant="primary">
                                    Proceed
								</Button>
                            </Modal.Footer>
                        </Modal.Dialog>
                    </Col>
                </Row>
            </Container>
        );
    }
}
