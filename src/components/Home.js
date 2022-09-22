import "./Home.css";
import { View } from "react-native";
import React, { useState, useEffect } from "react";
import { Button, ButtonGroup, Chip } from "@mui/material";
import { useNavigate } from "react-router-dom";

function Home() {
  const [images, setImages] = useState([]);

  useEffect(() => {
    fetch("/index").then((res) =>
      res.json().then((data) => {
        setImages(data);
      })
    );
  }, []);

  const navigate = useNavigate();

  const addHandler = () => navigate("/new_image");

  return (
    <div className="Home">
      <h1>
        <b>Neha George's Image Repository</b>
      </h1>
      <Button onClick={addHandler}>Add new image</Button>
      <View>
        <ul>
          {images.map((image) => {
            return (
              <div key={image[1]} style={{ border: "thin solid black" }}>
                <br></br>
                <Chip color="primary" label={image[1]} />
                <br></br>
                <br></br>
                <ButtonGroup
                  variant="outlined"
                  aria-label="outlined button group"
                >
                  <Button onClick={() => navigate(`/get_image/${image[1]}`)}>
                    View
                  </Button>
                  <Button onClick={() => navigate(`/update_image/${image[1]}`)}>
                    Update
                  </Button>
                  <Button onClick={() => navigate(`/delete_image/${image[1]}`)}>
                    Delete
                  </Button>
                </ButtonGroup>
                <br></br>
                <br></br>
              </div>
            );
          })}
        </ul>
      </View>
    </div>
  );
}

export default Home;
