import React, { Component } from "react";
import PropTypes, { InferProps } from "prop-types";

import Container from "react-bootstrap/Container";
// import * as toastr from "toastr";
import { Redirect } from "react-router-dom";

import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Modal from "react-bootstrap/Modal";
import { AuthService } from "../auth";
import { ComponentWithStore } from "../ui";

class Login extends Component<{}, any> {
    public authService: AuthService;
    static propTypes = {
        auth: PropTypes.shape({
            scope: PropTypes.string,
            profile: PropTypes.shape({
                preferred_name: PropTypes.string
            })
        })
    };
    static defaultProps: InferProps<typeof Login.propTypes> = {
        auth: {
            scope: null,
            profile: null
        }
    };

    constructor(props: any) {
        super(props);

        this.authService = new AuthService();
    }

    public login = () => {
        this.authService.login();
    };

    render() {
        const { auth }: InferProps<typeof Login.propTypes> = this.props;
        if (auth.profile) {
            return <Redirect to="/" />;
        }
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

export default ComponentWithStore(Login);
