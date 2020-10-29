import React from 'react';
import {getImages} from './getImages'
import { Button } from '@material-ui/core';
import ImageComponent from './Image';

const App = () => {

const [count, setCount] = React.useState(0);
const [allMovies,setAllMovies] = React.useState([] as string[]);
const [forwardButtonDisabled, setForwardButtonDisabled] = React.useState(false);
const [backwardButtonDisabled, setBackwardButtonDisabled] = React.useState(true);
const getAllData = getImages

React.useEffect(() => {
  const fetchData = async () =>{
    const arr:string[]= await getAllData("300")
    setAllMovies(arr)
    console.log(arr)
  }
  fetchData()
  },[]);

const handleForward = () =>{
  setCount(count+1)
  setForwardButtonDisabled(false)
  console.log(count)
  if (count === allMovies.length-2){
    setForwardButtonDisabled(true)
  }
  if (count === 0)
  {
    setBackwardButtonDisabled(false)
  }
}

const handleBackward = () =>{
  setCount(count-1)
  console.log(count)
  setBackwardButtonDisabled(false)
  if (count === 1){
    setBackwardButtonDisabled(true)
  }
  if (count === allMovies.length-1)
  {
    setForwardButtonDisabled(false)
  }
}

  return (
    <div className="App">
<div>
  <h1>{count+1}/{allMovies.length}</h1>
</div>
<div>
<ImageComponent link={allMovies[count]}/>
</div>
<div>
<Button variant="contained" color="primary" onClick={handleBackward} disabled={backwardButtonDisabled}>
  Back
</Button>
<Button variant="contained" color="primary" onClick={handleForward} disabled={forwardButtonDisabled}>
  Next
</Button> 
</div>
<div>
<Button size="large" color="default" variant="outlined">
  Large
</Button>
<Button variant="contained" color="secondary">
  CloseupShot
</Button> <Button variant="contained" color="secondary">
  Wide Shot
</Button> <Button variant="contained" color="secondary">
  Medium
</Button> 
</div>
</div>
  );
}

export default App;
