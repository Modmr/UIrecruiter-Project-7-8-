import * as React from 'react';

export class About extends React.Component<any, any>{
  constructor(props : any){
    super(props);
  }


  public render() {
    return (
        <div style={{height: 1500, marginTop: "50px"}}>
          <p>This is the about page, explaining about the digital assistant</p>
        </div>
    );
  }
}