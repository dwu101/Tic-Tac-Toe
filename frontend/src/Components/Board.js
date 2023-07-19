import React, { useState } from 'react';
import './Board.css'


export const Board = () => {

  const [buttonSettings, setbuttonSettings] = useState({
    'button00': {'disabled':false, 'color': 'white'},
    'button01': {'disabled':false, 'color': 'white'},
    'button02': {'disabled':false, 'color': 'white'},
    'button10': {'disabled':false, 'color': 'white'},
    'button11': {'disabled':true, 'color': 'red'},
    'button12': {'disabled':false, 'color': 'white'},
    'button20': {'disabled':false, 'color': 'white'},
    'button21': {'disabled':false, 'color': 'white'},
    'button22': {'disabled':false, 'color': 'white'},
  });


  const handleClick = (buttonId) => {
    setbuttonSettings((prevButtonStates) => ({
      ...prevButtonStates,
      [buttonId]: {'disabled':!prevButtonStates[buttonId], 'color' : 'green'} // Toggle the button state
      
    }));
  };

  const handleReset = () => {
    setbuttonSettings({
      'button00': {'disabled':false, 'color': 'white'},
      'button01': {'disabled':false, 'color': 'white'},
      'button02': {'disabled':false, 'color': 'white'},
      'button10': {'disabled':false, 'color': 'white'},
      'button11': {'disabled':true, 'color': 'red'},
      'button12': {'disabled':false, 'color': 'white'},
      'button20': {'disabled':false, 'color': 'white'},
      'button21': {'disabled':false, 'color': 'white'},
      'button22': {'disabled':false, 'color': 'white'},
    });
  };

  const buttonStyle = {
    margin: '10px',
    fontSize: '30px',

  }

  const rowStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  }

  const gridStyle = {
    display: 'flex',
    flexDirection: 'column',
  }

  return (
    <div style={gridStyle}>
        <div style={rowStyle}>
            <button disabled={buttonSettings['button00']['disabled']} onClick={ () => {handleClick('button00');}} style ={Object.assign({backgroundColor:buttonSettings['button00']['color']}, buttonStyle)}>0-0</button>
            <button disabled={buttonSettings['button01']['disabled']} onClick={ () => {handleClick('button01');}} style ={Object.assign({backgroundColor:buttonSettings['button01']['color']}, buttonStyle)}>0-1</button>            
            <button disabled={buttonSettings['button02']['disabled']} onClick={ () => {handleClick('button02');}} style ={Object.assign({backgroundColor:buttonSettings['button02']['color']}, buttonStyle)}>0-2</button>            
        </div>

        <div style={rowStyle}>
            <button disabled={buttonSettings['button10']['disabled']} onClick={ () => {handleClick('button10');}} style ={Object.assign({backgroundColor:buttonSettings['button10']['color']}, buttonStyle)}>1-0</button>
            <button disabled={buttonSettings['button11']['disabled']} onClick={ () => {handleClick('button11');}} style ={Object.assign({backgroundColor:buttonSettings['button11']['color']}, buttonStyle)}>1-1</button>            
            <button disabled={buttonSettings['button12']['disabled']} onClick={ () => {handleClick('button12');}} style ={Object.assign({backgroundColor:buttonSettings['button12']['color']}, buttonStyle)}>1-2</button>            
        </div>

        <div style={rowStyle}>
            <button disabled={buttonSettings['button20']['disabled']} onClick={ () => {handleClick('button20');}} style ={Object.assign({backgroundColor:buttonSettings['button20']['color']}, buttonStyle)}>2-0</button>
            <button disabled={buttonSettings['button21']['disabled']} onClick={ () => {handleClick('button21');}} style ={Object.assign({backgroundColor:buttonSettings['button21']['color']}, buttonStyle)}>2-1</button>            
            <button disabled={buttonSettings['button22']['disabled']} onClick={ () => {handleClick('button22');}} style ={Object.assign({backgroundColor:buttonSettings['button22']['color']}, buttonStyle)}>2-2</button>            
        </div>

        <div style = {rowStyle}>
            <button style ={buttonStyle} onClick = {handleReset} >reset</button>
        </div>

    </div>
  );
};

// export default Board;