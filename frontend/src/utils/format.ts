import live_scores_cricket from "../services/api/live_scores_cricket";

const data= await live_scores_cricket()
console.log("Response data",data)

