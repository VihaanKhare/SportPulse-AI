import { config } from 'dotenv';
config({ override: true });

export const mongodb_uri = process.env.MONGODB_URI as string;