// WaitingPage component for the loading screen
const WaitingPage = () => (
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Waiting Page</title>
        <style>
          {`
            body {
              display: flex;
              align-items: center;
              justify-content: center;
              height: 100vh;
              margin: 0;
              background-color: #FAEED1;
};
            }
  
            .loading-container {
              text-align: center;
            }
  
            .loading-spinner {
              border: 15px solid #f3f3f3;
              border-top: 15px solid #3498db;
              border-radius: 60%;
              width: 150px;
              height: 150px;
              animation: spin 1s linear infinite;
            }
  
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          `}
        </style>
      </head>
      <body>
        <div className="page" style={{display: "flex", flexDirection:"column", justifyContent:"center", alignItems:"center"}}>
          <div style={{ width: '100%', maxWidth: '1800px', marginBottom: '50px', boxSizing: 'border-box', display: 'flex', justifyContent: 'space-around' }}>
            <img style={{ width: '1000px', height: 'auto', borderRadius: '8px' }} src="https://bincy.fr/_next/image?url=https%3A%2F%2Fadmin.bincy.fr%2Fuploads%2Fbincy_rvb_cc17b25177.png&w=1920&q=75" alt="Bincy Logo" />
          </div>
          <div className="loading-container" style={{display: "flex", flexDirection:"column", justifyContent:"center", alignItems:"center"}}>
            <h1 style={{fontSize:"50px",marginTop:"100px", marginBottom:"100px"}}>The data are coming soon...</h1>
            <div className="loading-spinner"></div>
          </div>
        </div>
      </body>
    </html>
  );
  
  export default WaitingPage;