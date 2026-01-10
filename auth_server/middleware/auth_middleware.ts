import { auth } from 'express-oauth2-jwt-bearer'; 
import dotenv from 'dotenv';

dotenv.config();

export const jwtCheck = auth({
  audience: process.env.AUDIENCE,
  issuerBaseURL: process.env.ISSUER_BASE_URL,
  tokenSigningAlg: process.env.TOKEN_SIGNING_ALG,
});

