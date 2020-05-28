import React, { Component } from "react";
import PropTypes, { InferProps } from "prop-types";

import { Redirect } from "react-router-dom";

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

class Home extends Component<{}, any> {
    static propTypes = {
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

    static defaultProps: InferProps<typeof Home.propTypes> = {
        auth: {
            scope: null,
            profile: null
        }
    };

    render() {
        const { auth }: InferProps<typeof Home.propTypes> = this.props;
        return (
            <Container fluid="md">
                <Row>
                    {auth.profile ? (
                        <Col md={12}>
                            <h1>Hello {auth.profile.preferred_username}</h1>
                            <h2>Welcome to Fake NOM</h2>

                            <hr />

                            <Card
                                bg="light"
                                text={"dark"}
                                style={{ width: "18rem" }}
                            >
                                <Card.Header>Access Token</Card.Header>
                                <Card.Body>
                                    <Card.Title>For usage with API</Card.Title>
                                    <Card.Text>
                                        <Form.Control as="textarea" rows="3">
                                            {auth.access_token}
                                        </Form.Control>
                                    </Card.Text>
                                </Card.Body>
                            </Card>

                            <hr />
                            <h3>Your Session Metadata:</h3>

                            <p>
                                <pre>{JSON.stringify(auth, null, 4)}</pre>
                            </p>
                        </Col>
                    ) : (
                            <Redirect to="/login" />
                        )}
                </Row>
            </Container>
        );
    }
}

export default ComponentWithStore(Home);
