import React, { Component } from "react";

import Container from "react-bootstrap/Container";

import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Modal from "react-bootstrap/Modal";
import { AuthService } from "../auth";

export default class Logout extends Component<{}, any> {
    public authService: AuthService;

    constructor(props: any) {
        super(props);
        this.authService = new AuthService();
    }

    public logout = () => {
        this.authService.logout();
    };

    render() {
        return (
            <Container fluid="md">
                <Row>
                    <Col md={12}>
                        <Modal.Dialog>
                            <Modal.Header>
                                <Modal.Title>
                                    Do you really wish to logout?
								</Modal.Title>
                            </Modal.Header>

                            <Modal.Footer>
                                <Button onClick={this.logout} variant="danger">
                                    Logout
								</Button>
                            </Modal.Footer>
                        </Modal.Dialog>
                    </Col>
                </Row>
            </Container>
        );
    }
}
