import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import Container from "react-bootstrap/Container";

import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Modal from "react-bootstrap/Modal";
import { AuthService } from "../auth";
// import { ComponentWithStore } from "../ui";

type LogoutProps = {
    logout: () => {};
};

class Logout extends Component<LogoutProps> {
    public authService: AuthService;
    static propTypes = {
        logout: PropTypes.func,
        auth: PropTypes.shape({
            scope: PropTypes.string,
            access_token: PropTypes.string,
            id_token: PropTypes.string,
            refresh_token: PropTypes.string,
            profile: PropTypes.shape({
                preferred_username: PropTypes.string
            })
        })
    };

    constructor(props: LogoutProps) {
        super(props);
        this.authService = new AuthService();
    }

    public logout = () => {
        this.authService
            .logout()
            .then(() => {
                this.props.logout();
            })
            .catch(error => {
                console.log(error);
                this.props.logout();
            });
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
export default connect(
    state => {
        return { ...state };
    },
    {
        logout: function() {
            return {
                type: "LOGOUT"
            };
        }
    }
)(Logout);
