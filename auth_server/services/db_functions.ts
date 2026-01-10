import { db_connect } from "../configs/db_connection"

export const validate_user: (email:string)=>Promise<boolean> = async (email:string)=>{
  try{
    const conn = await db_connect()
    const collection = await conn.db("gc_tech_project_database").collection("users_preferences");
    const isPresent = await collection.findOne({"email":email});
    if(isPresent){
      return true;
    }else{
      return false;
    }
  }
  catch(err){
    console.error("Error checking for documents:", err);
    throw err;
  }
}

export const insertDocuments: (email:string, preferences:string[])=>Promise<void> = async (email:string, preferences:string[])=>{
  try{
    const conn = await db_connect()
    const collection = conn.db("gc_tech_project_database").collection("users_preferences");
    await collection.insertOne({"email":email, "preferences":preferences});
  }
  catch(err){
    console.error("Error inserting documents:", err);
    throw err;
  }
}

export const fetchPreferencesFromDB: (email:string)=>Promise<string[]> = async (email:string)=>{
  try{
    const conn = await db_connect()
    const collection = await conn.db("gc_tech_project_database").collection("users_preferences");
    const result = await collection.findOne({"email":email});
    if(result){
      return result.preferences;
    }else{
      return [];
    }
  }
  catch(err){
    console.error("Error fetching documents:", err);
    throw err;
  }
}