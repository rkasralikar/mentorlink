// TODO: get interest list.
const GetInterests = (req, res, next)=>{
    Models.Interest.find({}).then((interestList)=>{
        if(!interestList){
            return next(setError(MSG.DATA_NOT_FOUND));
        }else {
            return res.send({ data: interestList, message: MSG.DATA_FOUND });
        }
    }).catch((err)=>{
        console.log('Interest list err: ', err);
        return next(setError(MSG.INTERNAL_ERROR, 500));
    });
};

// TODO: save interest.
const SaveInterest = (req, res, next)=>{

    const interestArray = req.body;
    interestArray.map((interest) => Models.Interest.findOne({"name":interest.name},(err,cb)=>{
        console.log("Interests From Array-->>>",cb);
        if(cb == null || cb == ""){
            
            console.log("here-->>>>");
            const interests = new Models.Interest(
                {
                    name: interest.name,
                   
                }
            );
        console.log("interest for saving-->>",interest);
            interests.save((err)=>{
                if(err){
                    console.log("Interest save err: ", err);
                    return next(setError(MSG.INTERNAL_ERROR, 500));
                } else {
                    return res.send({ message: MSG.SUCCESS });
                }
            });
        }
    }));
  
   

    
};



module.exports = {
    GetInterests,
    SaveInterest
    
};
