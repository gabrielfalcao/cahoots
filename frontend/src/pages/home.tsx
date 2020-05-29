import React, { Component } from "react";
import PropTypes, { InferProps } from "prop-types";

import { Redirect } from "react-router-dom";
import { Dispatch } from "redux";

import Container from "react-bootstrap/Container";

import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
// import Button from "react-bootstrap/Button";
// import ButtonGroup from "react-bootstrap/ButtonGroup";
// import ListGroup from "react-bootstrap/ListGroup";
// import ProgressBar from "react-bootstrap/ProgressBar";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import { ComponentWithStore } from "../ui";

type ProfilePageProps = {
    dispatch: Dispatch;
};

class ProfilePage extends Component<ProfilePageProps> {
    static propTypes = {
        auth: PropTypes.shape({
            scope: PropTypes.string,
            access_token: PropTypes.string,
            id_token: PropTypes.string,
            refresh_token: PropTypes.string,
            profile: PropTypes.shape({
                preferred_username: PropTypes.string,
                email: PropTypes.string,
                jti: PropTypes.string,
                acr: PropTypes.string,
                name: PropTypes.string,
                sub: PropTypes.string,
                typ: PropTypes.string,
                aud: PropTypes.string,
                exp: PropTypes.string,
                given_name: PropTypes.string,
                family_name: PropTypes.string,
                nbf: PropTypes.string,
                azp: PropTypes.string,
                session_state: PropTypes.string,
                iss: PropTypes.string
            })
        })
    };

    static defaultProps: InferProps<typeof ProfilePage.propTypes> | any = {
        auth: {
            scope: null,
            profile: null
        }
    };

    render() {
        const { auth }: any = this.props;
        return (
            <Container fluid="md">
                <Row>
                    {auth.profile ? (
                        <React.Fragment>
                            <Col md={12}>
                                <h1>Hello {auth.profile.preferred_username}</h1>
                                <h2>Welcome to Fake NOM</h2>

                                <hr />
                            </Col>
                            <Col md={4}>
                                <Card
                                    bg="success"
                                    text={"white"}
                                    style={{ width: "18rem" }}
                                >
                                    <Card.Header>Access Token</Card.Header>
                                    <Card.Body>
                                        <Card.Title>
                                            For usage with API
										</Card.Title>
                                        <Card.Text>
                                            <Form.Control
                                                as="textarea"
                                                rows="3"
                                                readOnly
                                                value={auth.access_token}
                                            />
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                            <Col md={4}>
                                <Card
                                    bg="warning"
                                    text={"white"}
                                    style={{ width: "18rem" }}
                                >
                                    <Card.Header>Refresh Token</Card.Header>
                                    <Card.Body>
                                        <Card.Title>
                                            For usage with API
										</Card.Title>
                                        <Card.Text>
                                            <Form.Control
                                                as="textarea"
                                                rows="3"
                                                readOnly
                                                value={auth.refresh_token}
                                            />
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                            <Col md={4}>
                                <Card
                                    bg="info"
                                    text={"white"}
                                    style={{ width: "18rem" }}
                                >
                                    <Card.Header>Id Token</Card.Header>
                                    <Card.Body>
                                        <Card.Title>
                                            For usage with API
										</Card.Title>
                                        <Card.Text>
                                            <Form.Control
                                                as="textarea"
                                                rows="3"
                                                readOnly
                                                value={auth.id_token}
                                            />
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                            <Col md={12}>
                                <hr />
                                <h3>Scopes Allowed:</h3>

                                <strong>
                                    <pre className="text-info">
                                        {auth.scope}
                                    </pre>
                                </strong>
                            </Col>
                            <Col md={12}>
                                <hr />

                                <h3>ID Token claims:</h3>

                                <Form>
                                    {Object.keys(auth.profile).map(
                                        (key, index) => (
                                            <Form.Group
                                                as={Row}
                                                key={key}
                                                controlId={`form-control-${key}`}
                                            >
                                                <Form.Label column sm={2}>
                                                    {key}
                                                </Form.Label>
                                                <Col sm={10}>
                                                    <Form.Control
                                                        type="text"
                                                        readOnly
                                                        value={
                                                            auth.profile[key]
                                                        }
                                                    />
                                                </Col>
                                            </Form.Group>
                                        )
                                    )}
                                </Form>
                            </Col>
                        </React.Fragment>
                    ) : (
                            <Redirect to="/login" />
                        )}
                </Row>
            </Container>
        );
    }
}

export default ComponentWithStore(ProfilePage);
