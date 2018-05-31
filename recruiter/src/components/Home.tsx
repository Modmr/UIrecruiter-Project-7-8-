import * as React from 'react';

export class Home extends React.Component<any, any>{
  constructor(props : any){
    super(props);
  }


  public render() {
    return (
        <div style={{height: 1500, marginTop: "40px", marginLeft:-10}}>
          
          <iframe
          width="101%"
          height="40%"
          src="https://console.dialogflow.com/api-client/demo/embedded/d311c341-031c-413f-be25-47f1d828771a"/>

        </div>
    );
  }
}