import React, { Component } from "react";
import PropTypes from "prop-types";

import Container from "react-bootstrap/Container";

import Row from "react-bootstrap/Row";
import Jumbotron from "react-bootstrap/Jumbotron";
import Button from "react-bootstrap/Button";
// import ButtonGroup from "react-bootstrap/ButtonGroup";
// import ListGroup from "react-bootstrap/ListGroup";
// import ProgressBar from "react-bootstrap/ProgressBar";
// import Spinner from "react-bootstrap/Spinner";
import Col from "react-bootstrap/Col";
import { ComponentWithStore } from "../ui";

type HomeProps = {
    auth: any;
};

class Home extends Component<{}, any> {
    static propTypes = {
        auth: PropTypes.object
    };

    render() {
        console.log(this.props);
        return (
            <Container fluid="md">
                <Row>
                    <Col md={12}>
                        <br />
                        <br />
                        <h1>Welcome to Fake NOM!</h1>
                        <hr />
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default ComponentWithStore(Home);
