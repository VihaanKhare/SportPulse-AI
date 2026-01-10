import { fetchPreferencesFromDB, insertDocuments, validate_user } from "../services/db_functions";
import type { Request, Response } from "express";

export async function fetchPreferences(req:Request, res:Response) {
  try{
    console.log("Fetching preferences for user:", req.headers.email);
    const email = req.headers.email as string;
    const token = req.headers.authorization?.split(" ")[1] as string;
    console.log("Token:", token);
    console.log("Email:", email);
    const isRegistered = await validate_user(email);
    if(isRegistered === true){
      console.log("User is registered, fetching preferences...");
      const preferences = await fetchPreferencesFromDB(email);
      res.status(200).json(preferences);
    } else {
      res.status(200).json([]); }
  } catch(err){
    console.error("Error fetching preferences:", err);
    res.status(500).send("Internal Server Error");
  }
}

export async function savePreferences(req:Request, res:Response) {
  try{
    const email = req.headers.email as string;
    const preferences = req.body.preferences as string[];
    await insertDocuments(email, preferences);
    res.status(200).send("Preferences saved successfully");
  } catch(err){
    console.error("Error saving preferences:", err);
    res.status(500).send("Internal Server Error");
  }
}