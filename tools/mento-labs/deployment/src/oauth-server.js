const express = require('express');
const { createExpressHandler } = require('./oauth-api-handler-commonjs.js');

const app = express();
app.use(express.json());
app.use('/api', createExpressHandler());

const PORT = process.env.PORT || 3001;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`OAuth server running on port ${PORT}`);
});
