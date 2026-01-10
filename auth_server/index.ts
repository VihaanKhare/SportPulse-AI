import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import bodyParser from 'body-parser';
import cookieParser from 'cookie-parser';
import {router as protectedRoutes } from './routes/P_Routes.ts';
import {router as unprotectedRoutes } from './routes/UP_Routes.ts';
import { jwtCheck } from './middleware/auth_middleware.ts';
import { db_connect } from './configs/db_connection.ts';

db_connect()

const app = express();

app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'email'],
}));


const port = process.env.PORT;
dotenv.config();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());


// Import routes
app.use('/', jwtCheck ,  unprotectedRoutes);
app.use('/protected',protectedRoutes);

app.listen(3000, () => {
  console.log(`Auth server is running on port ${port}`);
}); 


