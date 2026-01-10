import { Router } from "express";
import { jwtCheck } from "../middleware/auth_middleware";
import { fetchPreferences, savePreferences } from "../controllers/user_controllers";


export const router = Router();

router.get("/signed_in", fetchPreferences);

router.post("/save_prefs",savePreferences);