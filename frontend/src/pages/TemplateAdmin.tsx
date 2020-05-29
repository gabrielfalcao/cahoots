import React, { Component } from "react";
import PropTypes, { InferProps } from "prop-types";

import Container from "react-bootstrap/Container";

import Row from "react-bootstrap/Row";
// import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
// import ButtonGroup from "react-bootstrap/ButtonGroup";
// import ListGroup from "react-bootstrap/ListGroup";
// import ProgressBar from "react-bootstrap/ProgressBar";
// import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import { ComponentWithStore } from "../ui";

type AuthProps = {
    scope: string;
};
type TemplateAdminProps = {
    auth: AuthProps;
};

class Scope {
    auth: AuthProps;
    constructor(auth: AuthProps) {
        this.auth = auth;
    }
    public matches(regex: RegExp): boolean {
        return this.auth.scope.match(regex) !== null;
    }
    public canRead(): boolean {
        return this.matches(/template:read/);
    }
    public canWrite(): boolean {
        return this.matches(/template:write/);
    }
}

class TemplateAdmin extends Component<TemplateAdminProps> {
    static propTypes = {
        auth: PropTypes.shape({
            access_token: PropTypes.string,
            scope: PropTypes.string
        })
    };

    static defaultProps: InferProps<typeof TemplateAdmin.propTypes> | any = {
        auth: {
            access_token: null,
            scope: ""
        }
    };

    render() {
        const { auth }: any = this.props;
        const scope = new Scope(auth);
        return (
            <Container fluid="md">
                <Row>
                    <Col md={12}>
                        <h1>Template Admin</h1>
                        <hr />
                        <p>
                            {scope.canRead() ? (
                                <Button variant="info">List Templates</Button>
                            ) : null}
                        </p>
                        <p>
                            {scope.canWrite() ? (
                                <Button variant="success">
                                    Create Template
                                </Button>
                            ) : null}
                        </p>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default ComponentWithStore(TemplateAdmin);
