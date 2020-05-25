import React, {
    useState // useEffect,
    // useCallback,
    // MouseEvent
} from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
// import Button from "react-bootstrap/Button";
// import ButtonGroup from "react-bootstrap/ButtonGroup";
// import ListGroup from "react-bootstrap/ListGroup";
// import ProgressBar from "react-bootstrap/ProgressBar";
// import Spinner from "react-bootstrap/Spinner";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
// import Authenticate from "react-openidconnect";

// var OidcSettings = {
//     authority:
//         "https://id.t.newstore.net/auth/realms/gabriel-NA-43928/protocol/openid-connect/auth",
//     client_id: "fake-nom",
//     redirect_uri: `${window.location}`,
//     response_type: "id_token token",
//     scope: "openid profile roles template:read template:write",
//     post_logout_redirect_uri: `${window.location}`
// };

const BACKEND_BASE_URL = "https://keycloak-fulltestco.ngrok.io";

// interface File {
//     readonly name: string;
//     readonly size: number;
// }

// const FILE_SERVER_BASE_URL =
//     document.location.protocol === "http:"
//         ? "https://localhost:5000"
//         : "https://keycloak.fulltest.co";

function App() {
    const [error] = useState(null);

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
                <Col>
                    <a href={`${BACKEND_BASE_URL}/login/oauth2`}>Login</a>
                </Col>
            </Row>
        </Container>
    );
}

export default App;
