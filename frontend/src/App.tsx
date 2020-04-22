import React, { useState, useEffect, useCallback, MouseEvent } from "react";

import { FlexGrid, FlexGridItem } from "baseui/flex-grid";
import { BlockProps } from "baseui/block";

import { Client as Styletron } from "styletron-engine-atomic";
import { Provider as StyletronProvider } from "styletron-react";
import { LightTheme, BaseProvider, styled } from "baseui";

import * as superagent from "superagent";

import { useDropzone } from "react-dropzone";
import CustomLink from "./components/CustomLink";
const itemProps: BlockProps = {
    backgroundColor: "mono300",
    height: "scale1000",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
};

const engine = new Styletron();
const Centered = styled("div", {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100%"
});

interface File {
    readonly name: string;
    readonly size: number;
}

function App() {
    const [progress, setProgress] = useState(0);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState(null);
    const [files, setFiles] = useState([]);
    const [uploads, setUploads] = useState([] as Array<File>);

    function doUpload(event: MouseEvent<HTMLButtonElement>) {
        let http = superagent.post("http://localhost:5000/upload");
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
    });
    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop
    });

    function listFiles() {
        superagent.get("http://localhost:5000/files").end((err, response) => {
            if (err) {
                setError(err);
            } else if (response.body) {
                setUploads(response.body as Array<File>);
            }
        });
    }
    return (
        <StyletronProvider value={engine}>
            <BaseProvider theme={LightTheme}>
                <FlexGrid
                    flexGridColumnCount={3}
                    flexGridColumnGap="scale800"
                    flexGridRowGap="scale800"
                    marginBottom="scale800"
                >
                    <FlexGridItem
                        {...itemProps}
                        overrides={{
                            Block: {
                                style: ({ $theme }) => ({
                                    width: `calc((200% - ${$theme.sizing.scale800}) / 3)`
                                })
                            }
                        }}
                    >
                        <CustomLink />
                    </FlexGridItem>
                    <FlexGridItem display="none">
                        This invisible one is needed so the margins line up
					</FlexGridItem>
                    <FlexGridItem {...itemProps}>Item</FlexGridItem>
                    <FlexGridItem {...itemProps}>Item</FlexGridItem>
                    <FlexGridItem {...itemProps}>Item</FlexGridItem>
                    <FlexGridItem {...itemProps}>Item</FlexGridItem>
                </FlexGrid>
            </BaseProvider>
        </StyletronProvider>
    );
}
export default App;
