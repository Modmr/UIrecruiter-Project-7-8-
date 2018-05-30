import './App.css';

import * as React from 'react';
import { Link, Route } from 'react-router-dom';

import { About } from './components/About';
import { Home } from './components/Home';


class App extends React.Component<any, any> {

  public render() {
    return (
      <div>
        <div className="navbar">
          <Link to="/">Home</Link>         
          <Link to="/About">About</Link>
        </div>
        
        <div>
        {/* note: <Route> is the place where the component will be rendered. */}
          <Route exact={true} path="/" component={Home}/>
          <Route path="/About" component={About}/>
        </div>
      </div>
    );
  }
}

export default App;
