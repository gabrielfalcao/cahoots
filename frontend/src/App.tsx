import React, { useState, useEffect, useCallback, MouseEvent } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import ListGroup from "react-bootstrap/ListGroup";
import ProgressBar from "react-bootstrap/ProgressBar";
import Spinner from "react-bootstrap/Spinner";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import * as superagent from "superagent";

import { useDropzone } from "react-dropzone";

interface File {
	readonly name: string;
	readonly size: number;
}

const FILE_SERVER_BASE_URL =
	document.location.protocol === "http:"
		? "https://localhost:5000"
		: "https://cahoots.in";

function load_cache(): Array<File> {
	const raw = window.localStorage.getItem("uploads");
	if (typeof raw === "string") {
		const items: Array<File> = JSON.parse(raw);
		return items;
	}
	return [];
}
function write_cache(items: Array<File>) {
	const value: string = JSON.stringify(items);
	window.localStorage.setItem("uploads", value);
	console.log("write_cache", value);
}

function clear_cache() {
	window.localStorage.removeItem("uploads");
}
function App() {
	const [progress, setProgress] = useState(0);
	const [isUploading, setIsUploading] = useState(false);
	const [error, setError] = useState(null);
	const [files, setFiles] = useState([]);
	const [uploads, setUploads] = useState(load_cache());

	function doUpload(event: MouseEvent<HTMLButtonElement>) {
		let http = superagent.post(`${FILE_SERVER_BASE_URL}/upload`);
		files.forEach(file => {
			http = http.attach("file", file);
		});
		http.on("progress", e => {
			if (e.direction === "upload" && e.percent) {
				setIsUploading(true);
				setProgress(e.percent);
				console.log(e);
			}
		}).end((err, response) => {
			setIsUploading(false);
			setProgress(0);
			setFiles([]);
			if (err) {
				setError(err);
			} else {
				setUploads(response.body);
				setError(null);
				write_cache(response.body);
			}
		});
		event.preventDefault();
	}
	const onDrop = useCallback(acceptedFiles => {
		setFiles(files => files.concat(acceptedFiles));
		setError(null);
	}, []);

	useEffect(() => {
		// Similar to componentDidMount and componentDidUpdate:
		document.title = "Personal File Server";

		const timer = setTimeout(() => {
			const cached = load_cache();
			if (cached.length === 0) {
				listFiles();
			}
		}, 1000);
		return () => clearTimeout(timer);
	});
	const { getRootProps, getInputProps, isDragActive } = useDropzone({
		onDrop
	});

	function listFiles() {
		superagent.get(`${FILE_SERVER_BASE_URL}/files`).end((err, response) => {
			if (err) {
				setError(err);
			} else if (response.body) {
				setUploads(response.body as Array<File>);
				setError(null);
				write_cache(response.body);
			}
		});
	}
	return (
		<Container fluid="md">
			{error !== null ? (
				<Row>
					<Col md={12}>
						<Card bg={"danger"} text="white">
							<Card.Body {...getRootProps()}>
								<Card.Title>Error</Card.Title>
								<Card.Text>{`${error}`}</Card.Text>
							</Card.Body>
						</Card>
					</Col>
				</Row>
			) : null}
			<Row>
				<Col md={12}>
					<ListGroup>
						{uploads.map(file => {
							if ("name" in file) {
								return (
									<ListGroup.Item key={file.name}>
										<a
											target="_blank"
											rel="noopener noreferrer"
											href={`${FILE_SERVER_BASE_URL}/uploads/${file.name}`}
										>
											{file.name}
										</a>
									</ListGroup.Item>
								);
							} else {
								return null;
							}
						})}
						<ListGroup.Item>
							<Row>
								<Col md={12}>{uploads.length} files</Col>
							</Row>
							<Row>
								<Col md={9}></Col>
								<Col md={3}>
									<ButtonGroup>
										<Button onClick={listFiles}>
											List Files
										</Button>
										<Button
											variant="danger"
											onClick={() => {
												clear_cache();
												setUploads([]);
											}}
										>
											Clear Cache
										</Button>
									</ButtonGroup>
								</Col>
							</Row>
						</ListGroup.Item>
					</ListGroup>
				</Col>
			</Row>
			<Row>
				<Col md={12}>
					<Card>
						{files.length === 0 ? (
							<Card.Body {...getRootProps()}>
								<Card.Title>Upload Files</Card.Title>
								<input {...getInputProps()} />

								{isDragActive ? (
									<Card.Text>
										Drop the files here ...
									</Card.Text>
								) : (
									<Card.Text>
										Drag 'n' drop some files here, or click
										to select files.
									</Card.Text>
								)}
							</Card.Body>
						) : isUploading ? null : (
							<Card.Body>
								<h1>Ready to upload!</h1>
							</Card.Body>
						)}

						{files.length > 0 ? (
							<Card.Body>
								{isUploading ? (
									<Card.Text>
										<Spinner
											animation="grow"
											variant="dark"
										/>
										Uploading ...
									</Card.Text>
								) : (
									<Button onClick={doUpload}>
										Upload {files.length} file(s)
									</Button>
								)}
							</Card.Body>
						) : null}
					</Card>
				</Col>
				<Col sm></Col>
			</Row>
			{progress > 0 ? (
				<Row>
					<Col>
						<ProgressBar now={progress} label={`${progress}%`} />
					</Col>
				</Row>
			) : null}
			<Row>
				<Col>
					<a href="/login/oauth2">Login</a>
				</Col>
			</Row>
		</Container>
	);
}

export default App;
