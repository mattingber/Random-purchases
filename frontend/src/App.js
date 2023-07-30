import React, { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const [formData, setFormData] = useState({
    userid: '',
    username: '',
    price: '',
  });

  const [getUserPurchasesId, setGetUserPurchasesId] = useState(''); // Separate state for "Get Purchases" form
  const [userPurchases, setUserPurchases] = useState([]); // State to hold retrieved purchases

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async () => {
    try {
      // Send POST request to web-gateway to create purchase
      const response = await axios.post('http://127.0.0.1:8100/userbuys', formData);
      console.log('UserBuy data has been posted:', response.data);
      toast.success('Random Item purchases sent successfuly!');
    } catch (error) {
      console.error('Error posting UserBuy data:', error);
      toast.error('Error Randomly purchasing item.');
    }
  };

  const handleGetPurchases = async () => {
    try {
      // Send GET request to web-gateway for getting purchases for the specific user
      const response = await axios.get(`http://127.0.0.1:8100/userbuys/${getUserPurchasesId}`);
      console.log(`Getting purchases for User ID: ${getUserPurchasesId}`, response.data);
      setUserPurchases(response.data); // Save the retrieved purchases in state
      response.data.length === 0 ? toast.error(`userID  ${getUserPurchasesId} has no purchase requests` ) : toast.success(`Retrieved purchases for User ID: ${getUserPurchasesId}`);
    } catch (error) {
      toast.error(`Error getting purchases for userID  ${getUserPurchasesId}` );
      console.error('Error getting purchases:', error);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h1>User Purchases</h1>
      <div style={{ display: 'flex', gap: '10px' }}>
        <TextField label="User ID" name="userid" value={formData.userid} onChange={handleChange} />
        <TextField label="Username" name="username" value={formData.username} onChange={handleChange} />
        <TextField label="Price" name="price" value={formData.price} onChange={handleChange} />
      </div>
      <Button variant="contained" color="primary" onClick={async () => await handleSubmit()}>
        PURCHASE RANDOM ITEM 
      </Button>
      <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
        <TextField
          label="Get Purchases for User ID"
          value={getUserPurchasesId}
          onChange={(e) => setGetUserPurchasesId(e.target.value)}
        />
        <Button variant="contained" color="secondary" onClick={async () => await handleGetPurchases()}>
          Get Purchases for User
        </Button>
      </div>
      {/* Display the retrieved purchases */}
      <div style={{ marginTop: '20px' }}>
        <h2>Retrieved Purchases:</h2>
        <ul>
          {userPurchases.map((purchase) => (
            <li key={purchase.id}>
              <strong>User </strong> {purchase.username}({purchase.userid}) bought a random item for <strong>${purchase.price}</strong>
            </li>
          ))}
        </ul>
      </div>

      {/* Toast notifications */}
      <ToastContainer />
    </div>
  );
}

export default App;
