const express=require("express");
const app=express();
const port=3000;
const images=30;
app.post(`/getdick:id([0-9]+)`, (req,res)=>{
    if(req.params.id==undefined){
    try{
        let random = Math.floor( Math.random() * images );
        res.json({message:"ちんこ",url:`http://localhost:${port}/TNK/${random}`,imageNo:`${random}`});
    }catch(err){
        res.status(500).send("Error");
        }
    }else{
        try{
            res.json({message:"ちんこ",url:`http://localhost:${port}/TNK/${req.params.id}`,imageNo:`${req.params.id}`});
        }catch(err){
            res.status(500).send("Error");
            }  
        }
    });
app.listen(port,()=>{
    console.log("started");
})


