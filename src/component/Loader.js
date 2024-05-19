import React from 'react';
import "./Loader.css"
import ScaleLoader from "react-spinners/ScaleLoader";

const Loader = () => {

  return (
    <div>
        <ScaleLoader color='rgb(227, 123, 88)' size={25}/>
    </div>

  );
};

export default Loader;
