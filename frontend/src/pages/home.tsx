import React, { Component } from "react";

import Container from "react-bootstrap/Container";

import Row from "react-bootstrap/Row";
// import Button from "react-bootstrap/Button";
// import ButtonGroup from "react-bootstrap/ButtonGroup";
// import ListGroup from "react-bootstrap/ListGroup";
// import ProgressBar from "react-bootstrap/ProgressBar";
// import Spinner from "react-bootstrap/Spinner";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";

// the clock's state has one field: The current time, based upon the
// JavaScript class Date
type ClockState = {
    time: Date;
    error: Error | null;
};
export default class Home extends Component<{}, ClockState> {
    // The tick function sets the current state. TypeScript will let us know
    // which ones we are allowed to set.
    tick() {
        this.setState({
            time: new Date()
        });
    }

    // Before the component mounts, we initialise our state
    componentWillMount() {
        this.tick();
        this.setState({ error: null });
    }

    // After the component did mount, we set the state each second.
    componentDidMount() {
        // setInterval(() => this.tick(), 1000);
    }

    // render will know everything!
    render() {
        const { error } = this.state;
        return (
            <Container fluid="md">
                {error !== null ? (
                    <Row>
                        <Col md={12}>
                            <Card bg={"danger"} text="white">
                                <Card.Body>
                                    <Card.Title>Error</Card.Title>
                                    <Card.Text>{`${error}`}</Card.Text>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                ) : null}

                <Row>
                    <Col md={12}>
                        <Card bg={"success"} text="white">
                            <Card.Body>
                                <Card.Title>FakeNOM</Card.Title>
                                <Card.Text>Hello</Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        );
    }
}
